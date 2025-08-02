# Detroit Event Aggregator

This project is a comprehensive event aggregation system for the Detroit metropolitan area. It automatically discovers local venues, scrapes event information from a variety of sources, and presents the data through a clean, searchable web interface.

## Key Features

- **Automated Venue Discovery:** The system uses the Google Places API to find event venues (stadiums, theaters, clubs, etc.) within a specified radius of a given location.
- **Intelligent Data Enrichment:** For each discovered venue, the system performs a web search to find its official website and social media pages. It then uses a Large Language Model (LLM) to intelligently extract detailed descriptions, social media handles, and other relevant information from the website content.
- **Multi-Source Event Scraping:** The event scraper gathers information from:
    - **Major Ticketing APIs:** Ticketmaster and Eventbrite.
    - **Local Event Listings:** Scrapes data from the "Visit Detroit" website.
    - **Individual Venue Websites:** Uses a headless browser to render dynamic pages and an LLM to extract structured event data from the raw HTML.
- **Data Deduplication:** A fuzzy matching algorithm is used to identify and remove duplicate events that may be listed on multiple platforms.
- **Web-Based Frontend:** A simple and clean web interface, built with vanilla JavaScript and styled with Tailwind CSS, allows users to view and filter upcoming events.

## Setup and Run

### 1. Environment Setup

**a. Create and Activate Virtual Environment:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**b. Install Dependencies:**

```bash
pip install -r requirements.txt
```

**c. Set Up Environment Variables:**

Create a `.env` file in the root directory and add your API keys:

```
GOOGLE_MAPS_API_KEY="YOUR_GOOGLE_MAPS_API_KEY"
TICKETMASTER_CONSUMER_KEY="YOUR_TICKETMASTER_API_KEY"
EVENTBRITE_API_KEY="YOUR_EVENTBRITE_API_KEY"
GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
```

### 2. Populate the Venue Database

To begin, you need to populate the database with venues. This is done using the `venue_database_agent.py` script.

```bash
python3 src/venue_database_agent.py --address "Detroit, MI" --radius 10
```

This command will find all venues within a 10-mile radius of Detroit, enrich their data, and save them to the `data/venues.db` database.

### 3. Scrape for Events

Once the venues are in the database, you can scrape for events using the `event_scraper_agent.py` script.

```bash
python3 src/event_scraper_agent.py
```

This will iterate through all the venues in the database and use the various scraping methods to find upcoming events. The results are then saved to the database.

### 4. View the Data on the Frontend

To view the collected data, you need to run the backend and frontend servers.

**a. Start the Backend Server:**

```bash
FLASK_APP=src/app.py python3 -m flask run &
```

**b. Start the Frontend Server:**

```bash
python3 -m http.server --directory frontend 8000 &
```

Once both servers are running, you can open your web browser and navigate to **http://localhost:8000** to view the event listings.

## Database Backup

To create a backup of the `venues.db` database, run the following command from the root directory:

```bash
./backup_db.sh
```

This will create a timestamped backup file in the `data/backups/` directory. The script will also automatically remove backups that are older than 7 days.

### 5. Deactivating the Application

To stop the servers, you can use the `jobs` command to find the process IDs and `kill` to terminate them.

To deactivate the virtual environment:

```bash
deactivate
```
