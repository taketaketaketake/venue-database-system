# src/event_scraper_agent.py

import sys
import os
from pathlib import Path
# Add project root to sys.path
sys.path.append(str(Path(__file__).parent.parent))

import click
import logging
import requests
from src.utils.db_utils import connect_db, execute_query, close_db
from src.utils.scraping_utils import scrape_website, scrape_dynamic_website
from src.utils.llm_utils import extract_event_data
from src.utils.validation_utils import deduplicate_events
from dotenv import load_dotenv

# Setup logging
Path('data/logs').mkdir(parents=True, exist_ok=True)
logging.basicConfig(filename='data/logs/errors.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()
TICKETMASTER_API_KEY = os.getenv('TICKETMASTER_CONSUMER_KEY')
EVENTBRITE_API_KEY = os.getenv('EVENTBRITE_API_KEY')

def get_api_events(venue_name):
    """
    Fetch events from Ticketmaster and Eventbrite APIs for a given venue.
    
    Args:
        venue_name (str): Venue name.
    
    Returns:
        list: List of events (name, date, url, venue).
    """
    try:
        events = []
        # Ticketmaster API
        url = f"https://app.ticketmaster.com/discovery/v2/events.json?apikey={TICKETMASTER_API_KEY}&keyword={venue_name}&city=Detroit"
        response = requests.get(url).json()
        for event in response.get('_embedded', {}).get('events', []):
            events.append({
                'name': event['name'],
                'date': event['dates']['start']['dateTime'],
                'url': event['url'],
                'venue': venue_name
            })
        # Eventbrite API
        url = f"https://www.eventbriteapi.com/v3/events/search/?q={venue_name}&location.address=Detroit&token={EVENTBRITE_API_KEY}"
        response = requests.get(url).json()
        for event in response.get('events', []):
            events.append({
                'name': event['name']['text'],
                'date': event['start']['local'],
                'url': event['url'],
                'venue': venue_name
            })
        logging.info(f"Fetched {len(events)} events for {venue_name} from APIs")
        return events
    except Exception as e:
        logging.error(f"API error for {venue_name}: {e}")
        return []

def get_local_events():
    """
    Scrape non-venue events from local sources (e.g., Visit Detroit).
    
    Returns:
        list: List of events (name, date, url, venue).
    """
    try:
        # Placeholder for scraping Visit Detroit
        # TODO: Implement Scrapy spider for https://visitdetroit.com
        logging.info("Scraping local events from Visit Detroit")
        return []
    except Exception as e:
        logging.error(f"Local events scraping error: {e}")
        return []

@click.command()
def scrape_events():
    """
    Scrape events daily and update the database.
    """
    try:
        logging.info("Starting event scraping")
        conn = connect_db()
        
        # Get all venues
        venues = execute_query(conn, "SELECT name, website_url, instagram, facebook, non_venue_flag FROM venues")
        if not venues:
            logging.warning("No venues found in database")
            print("Error: No venues found in database.")
            close_db(conn)
            return
        
        all_events = []
        for venue in venues:
            venue_name = venue['name']
            events = []
            
            # Skip non-venue locations for API/website scraping
            if not venue['non_venue_flag']:
                # API events
                events.extend(get_api_events(venue_name))
                
                # Website events
                if venue['website_url']:
                    website_events = scrape_website(venue['website_url'])
                    for event in website_events:
                        event['venue'] = venue_name
                    events.extend(website_events)
                
                # Dynamic website/X posts with Gemini
                if venue['website_url'] or venue['instagram'] or venue['facebook']:
                    dynamic_events = scrape_dynamic_website(venue['website_url'] or venue['instagram'] or venue['facebook'], extract_event_data)
                    for event in dynamic_events:
                        event['venue'] = venue_name
                    events.extend(dynamic_events)
            
            all_events.extend(events)
        
        # Non-venue events
        all_events.extend(get_local_events())
        
        # Deduplicate events
        all_events = deduplicate_events(all_events)
        
        # Update database
        for event in all_events:
            query = """
                UPDATE venues
                SET upcoming_event_name = ?, upcoming_event_date = ?, upcoming_event_page_url = ?, last_updated = CURRENT_TIMESTAMP
                WHERE name = ?
            """
            params = (event['name'], event['date'], event['url'], event['venue'])
            execute_query(conn, query, params)
            logging.info(f"Updated event for {event['venue']}: {event['name']}")
        
        conn.commit()
        close_db(conn)
        print(f"Successfully updated {len(all_events)} events in the database.")
        logging.info(f"Completed event scraping: {len(all_events)} events")
    
    except Exception as e:
        logging.error(f"Error in scrape_events: {e}")
        print(f"Error: {e}")

if __name__ == '__main__':
    scrape_events()