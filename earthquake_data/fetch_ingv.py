"""
INGV API Fetcher Module.

This module is responsible for retrieving earthquake data from the 
National Institute of Geophysics and Volcanology (INGV).
"""
import csv
import requests
import os
from datetime import datetime, timedelta


def gather_earthquakes(days):
    """
    Fetches earthquake data from the INGV API for the specified number of days.

    Args:
        days (int): Number of days in the past to query.

    Returns:
        list: A list of tuples (day, time, mag, lat, lon, place).
    """
    bounding_box = {}

    # Path handling to find 'bounding_box.csv'
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Look one level up (project root)
    csv_path = os.path.join(os.path.dirname(current_dir), 'bounding_box.csv')

    if not os.path.exists(csv_path):
        # Fallback to package dir
        csv_path = os.path.join(current_dir, 'bounding_box.csv')

    try:
        with open(csv_path, mode='r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                bounding_box[row['key']] = float(row['value'])
    except FileNotFoundError:
        print(f"Error: 'bounding_box.csv' not found. Please run write_bounding_box.py.")
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
        response = requests.get(url, params=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to INGV: {e}")
        return []

    data = response.json()
    events = data.get("features", [])
    earthquakes_list = []

    # Parsing JSON response
    for event in events:
        props = event["properties"]
        geom = event["geometry"]

        time_raw = props["time"]  # Format example: "2025-01-01T12:00:00.123Z"

        if isinstance(time_raw, str):
            clean_time = time_raw[:19]  # Strip milliseconds/Z for compatibility
            try:
                dt_object = datetime.fromisoformat(clean_time)

                earthquakes_list.append((
                    dt_object.strftime("%Y-%m-%d"),
                    dt_object.strftime("%H:%M:%S"),
                    props["mag"],
                    geom["coordinates"][1],  # Latitude
                    geom["coordinates"][0],  # Longitude
                    props["place"]
                ))
            except ValueError:
                continue

    return earthquakes_list

