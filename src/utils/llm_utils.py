import requests
from dotenv import load_dotenv
import os
import logging
import json

load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

def extract_venue_details(text):
    try:
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        headers = {'Content-Type': 'application/json'}
        prompt = f"""
        Given the following venue information: {text}
        Extract:
        - Size (Large: >10,000 capacity, Medium: 1,000-10,000, Small: <1,000)
        - Description (brief, max 100 words)
        - Instagram handle
        - Facebook page
        - Website URL
        - Non-venue flag (True if not a fixed venue, e.g., festival space)
        Return a JSON object with these fields. If data is unavailable, use reasonable defaults or null.
        """
        data = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.7}
        }
        response = requests.post(f"{url}?key={GEMINI_API_KEY}", headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        content = result['candidates'][0]['content']['parts'][0]['text']
        content = content.strip().strip('```json\n').strip('```')
        details = json.loads(content)
        logging.info(f"Extracted venue details for: {text}")
        return details
    except Exception as e:
        logging.error(f"Gemini API error for venue details: {e}")
        return {
            'size': 'Medium',
            'description': 'Unknown venue',
            'instagram': None,
            'facebook': None,
            'website_url': None,
            'non_venue_flag': False
        }

def extract_event_data(text, url):
    try:
        url_api = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        headers = {'Content-Type': 'application/json'}
        prompt = f"""
        Given the following text from {url}: {text[:1000]}...
        Extract a list of events with:
        - Name (event title)
        - Date (YYYY-MM-DD HH:MM:SS format)
        - URL (event page or source URL)
        Return a JSON array of objects with these fields. If no events, return an empty array.
        """
        data = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.7}
        }
        response = requests.post(f"{url_api}?key={GEMINI_API_KEY}", headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        content = result['candidates'][0]['content']['parts'][0]['text']
        content = content.strip().strip('```json\n').strip('```')
        events = json.loads(content)
        logging.info(f"Extracted {len(events)} events from: {url}")
        return events
    except Exception as e:
        logging.error(f"Gemini API error for events: {e}")
        return []
