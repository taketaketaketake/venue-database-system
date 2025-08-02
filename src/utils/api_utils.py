# src/utils/api_utils.py
import requests
from dotenv import load_dotenv
import os
from pathlib import Path
import click

load_dotenv()
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

def geocode_address(address):
    """
    Geocode an address using Google Maps API.
    
    Args:
        address (str): Address to geocode.
    
    Returns:
        tuple: (latitude, longitude) or None if geocoding fails.
    """
    try:
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={GOOGLE_MAPS_API_KEY}"
        response = requests.get(url).json()
        if response['status'] == 'OK':
            location = response['results'][0]['geometry']['location']
            return location['lat'], location['lng']
        else:
            print(f"Geocoding error for {address}: {response['status']}")
            return None
    except Exception as e:
        print(f"Geocoding request error: {e}")
        return None

def find_venues(latitude, longitude, radius_miles, categories=['stadium', 'theater', 'concert_hall', 'park', 'community_center', 'night_club', 'event_venue', 'museum', 'performing_arts_theater']):
    """
    Find venues near a location using Google Places API.
    
    Args:
        latitude (float): Latitude of the center point.
        longitude (float): Longitude of the center point.
        radius_miles (float): Search radius in miles.
        categories (list): List of venue types from Google Places API Table A.
    
    Returns:
        list: List of venue dictionaries (name, address, x_coordinate, y_coordinate, category, place_id).
    """
    try:
        radius_meters = radius_miles * 1609.34
        venues = []
        # If categories is empty, use default event-relevant types
        if not categories:
            categories = ['stadium', 'theater', 'concert_hall', 'park', 'community_center', 'night_club', 'event_venue', 'museum', 'performing_arts_theater']
        for category in categories:
            url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius={radius_meters}&type={category}&key={GOOGLE_MAPS_API_KEY}"
            response = requests.get(url).json()
            if response['status'] == 'OK':
                for place in response.get('results', []):
                    place_types = place.get('types', [])
                    venue = {
                        'name': place.get('name', ''),
                        'address': place.get('vicinity', ''),
                        'x_coordinate': place['geometry']['location']['lat'],
                        'y_coordinate': place['geometry']['location']['lng'],
                        'category': place_types[0] if place_types else 'unknown',
                        'place_id': place.get('place_id', '')  # Added place_id
                    }
                    venues.append(venue)
        return venues
    except Exception as e:
        print(f"Places API error: {e}")
        return []

def get_place_details(place_id):
    """
    Fetch detailed information for a venue using Google Places API Place Details.
    
    Args:
        place_id (str): The unique identifier for the place.
    
    Returns:
        dict: Dictionary containing website, phone_number, and rating, or None if not available.
    """
    try:
        url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=website,formatted_phone_number,rating&key={GOOGLE_MAPS_API_KEY}"
        response = requests.get(url).json()
        if response['status'] == 'OK':
            details = {
                'website': response['result'].get('website'),
                'phone_number': response['result'].get('formatted_phone_number'),
                'rating': response['result'].get('rating')
            }
            return {k: v for k, v in details.items() if v is not None}  # Return only non-None values
        else:
            print(f"Place Details error for place_id {place_id}: {response['status']}")
            return {'website': None, 'phone_number': None, 'rating': None}
    except Exception as e:
        print(f"Place Details request error: {e}")
        return {'website': None, 'phone_number': None, 'rating': None}