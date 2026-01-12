"""
Earthquakes Fetcher Module.

Provides functionality to fetch earthquake data from the USGS API.
"""
import datetime
import json
import requests

USGS_URL = (
    'https://earthquake.usgs.gov/fdsnws/event/1/query?'
    'starttime={}&format=geojson&limit=20000'
)


def get_earthquake(days_past):
    """
    Fetch earthquakes from the last 'days_past' days.

    Returns the one with the highest magnitude.

    Args:
        days_past (int): Number of days in the past to search.

    Returns:
         tuple: A tuple (magnitude, place) of the largest earthquake.
    """
    # Get the date of today - days_past days at 00 AM
    start_date = (
        datetime.datetime.now() + datetime.timedelta(days=-days_past)
    ).strftime("%Y-%m-%d")

    url = USGS_URL.format(start_date)
    response = requests.get(url, timeout=100)
    events = json.loads(response.text)
    max_magnitude = 0.0
    place = ''

    for event in events['features']:
        try:
            mag = float(event['properties']['mag'])
        except (TypeError, ValueError):
            continue  # Skip invalid data

        if mag > max_magnitude:
            max_magnitude = mag
            place = event['properties']['place']

    return max_magnitude, place
