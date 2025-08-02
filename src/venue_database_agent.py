# src/venue_database_agent.py
import sys
import logging
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import click
from src.utils.db_utils import connect_db, execute_query, close_db
from src.utils.api_utils import geocode_address, find_venues, get_place_details
from src.utils.llm_utils import extract_venue_details

# Setup logging
Path('data/logs').mkdir(parents=True, exist_ok=True)
logging.basicConfig(filename='data/logs/venue.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def update_venue_details(venue):
    """
    Update venue details using Google Places API and Gemini API.
    
    Args:
        venue (dict): Venue dictionary with name, address, category, and place_id.
    
    Returns:
        dict: Updated venue with size, description, instagram, facebook, website_url, phone_number, rating, non_venue_flag.
    """
    try:
        # Fetch details from Google Places API
        place_details = get_place_details(venue['place_id'])
        website = place_details.get('website')
        phone_number = place_details.get('phone_number')
        rating = place_details.get('rating')

        # Use Gemini API for remaining details
        text = f"{venue['name']}, {venue['address']}, {venue['category']}"
        details = extract_venue_details(text)
        venue.update({
            'size': details['size'],
            'description': details['description'],
            'instagram': details['instagram'],
            'facebook': details['facebook'],
            'non_venue_flag': details['non_venue_flag']
        })
        
        return venue
    except Exception as e:
        logging.error(f"Error updating venue details for {venue['name']}: {e}")
        return venue

@click.command()
@click.option('--address', required=True, help='Address to search near')
@click.option('--radius', default=10, type=float, help='Radius in miles')
def update_venues(address, radius):
    """
    Update venues in the database based on address and radius.
    """
    try:
        logging.info(f"Starting venue update for {address} with radius {radius} miles")
        conn = connect_db()
        
        # Geocode the address
        coordinates = geocode_address(address)
        if not coordinates:
            print(f"Error: Could not geocode address {address}")
            close_db(conn)
            return
        
        latitude, longitude = coordinates
        venues = find_venues(latitude, longitude, radius)
        
        if not venues:
            print("No venues found.")
            close_db(conn)
            return
        
        updated_count = 0
        for venue in venues:
            venue = update_venue_details(venue)
            query = """
                INSERT OR REPLACE INTO venues (
                    name, x_coordinate, y_coordinate, address, size, category, 
                    description, instagram, facebook, website_url, phone_number, rating, non_venue_flag
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            params = (
                venue['name'], venue['x_coordinate'], venue['y_coordinate'], 
                venue['address'], venue.get('size'), venue['category'], 
                venue.get('description'), venue.get('instagram'), 
                venue.get('facebook'), venue.get('website_url'), 
                venue.get('phone_number'), venue.get('rating'), 
                venue.get('non_venue_flag', False)
            )
            execute_query(conn, query, params)
            updated_count += 1
            logging.info(f"Updated venue: {venue['name']}")
        
        conn.commit()
        close_db(conn)
        print(f"Successfully updated {updated_count} venues in the database.")
        logging.info(f"Completed venue update: {updated_count} venues")
    
    except Exception as e:
        logging.error(f"Error in update_venues: {e}")
        print(f"Error: {e}")

if __name__ == '__main__':
    update_venues()