"""
INGV API Fetcher Module.

This module retrieves earthquake data from the INGV Institute.
INGV: National Institute of Geophysics and Volcanology.
"""
import os
import csv
from datetime import datetime, timedelta
import requests

# gather_earthquakes is divided in 3 functions to solve pylint:
# 'too many local variables 22/15'


def _load_bounding_box():
    """Load bounding box coordinates from CSV file."""
    bounding_box = {}
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Look one level up (project root)
    csv_path = os.path.join(os.path.dirname(current_dir), 'bounding_box.csv')

    if not os.path.exists(csv_path):
        # Fallback to package dir
        csv_path = os.path.join(current_dir, 'bounding_box.csv')

    if not os.path.exists(csv_path):
        print(
            "Error: 'bounding_box.csv' not found. "
            "Please run write_bounding_box.py."
        )
        return None

    with open(csv_path, mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            bounding_box[row['key']] = float(row['value'])

        return bounding_box


def _parse_event(event):
    """Parse a single earthquake event from JSON."""
    props = event["properties"]
    geom = event["geometry"]
    time_raw = props["time"]
    # time_raw format example: 2025-01-01T12:00:00.123Z

    if not isinstance(time_raw, str):
        return None

    # Strip milliseconds/Z for compatibility
    clean_time = time_raw[:19]
    try:
        # Date object
        dt_object = datetime.fromisoformat(clean_time)
        return (
            dt_object.strftime("%Y-%m-%d"),
            dt_object.strftime("%H:%M:%S"),
            props["mag"],
            geom["coordinates"][1],  # Latitude
            geom["coordinates"][0],  # Longitude
            props["place"]
                )

    except ValueError:
        return None


def gather_earthquakes(days):
    """
    Fetch earthquake data from the INGV API for the specified number of days.

    Args:
        days (int): Number of days in the past to query.

    Returns:
        list: A list of tuples (day, time, mag, lat, lon, place).
    """
    bounding_box = _load_bounding_box()
    if not bounding_box:
        return []

    # Preparing API Request
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=days)
    url = "https://webservices.ingv.it/fdsnws/event/1/query?"

    params = {
        "format": "geojson",
        "starttime": start_time.strftime("%Y-%m-%d"),
        "endtime": end_time.strftime("%Y-%m-%d"),
        "minlatitude": bounding_box.get('minlatitude'),
        "maxlatitude": bounding_box.get('maxlatitude'),
        "minlongitude": bounding_box.get('minlongitude'),
        "maxlongitude": bounding_box.get('maxlongitude')
    }

    try:
        response = requests.get(url, params=params, timeout=100)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to INGV: {e}")
        return []

    data = response.json()
    events = data.get("features", [])
    earthquakes_list = []

    for event in events:
        parsed = _parse_event(event)
        if parsed:
            earthquakes_list.append(parsed)

    return earthquakes_list
