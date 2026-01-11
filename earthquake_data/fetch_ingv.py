import csv
import requests
from datetime import datetime, timedelta
import os

def gather_earthquakes(days):
    bounding_box = {}

    # 1. READ THE CSV SAFELY
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, 'bounding_box.csv')

    # You can keep comments like this, they are helpful!
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            key = row["key"]
            value = float(row["value"])
            bounding_box[key] = value

    # 2. PREPARE THE QUERY
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=days)

    url = "https://webservices.ingv.it/fdsnws/event/1/query"

    params = {
        "format": "geojson",
        "starttime": start_time.strftime("%Y-%m-%d"),
        "endtime": end_time.strftime("%Y-%m-%d"),
        "minlatitude": bounding_box["minlatitude"],
        "maxlatitude": bounding_box["maxlatitude"],
        "minlongitude": bounding_box["minlongitude"],
        "maxlongitude": bounding_box["maxlongitude"],
    }

    # 3. REQUEST THE DATA
    # (Debug prints removed here for final submission)
    response = requests.get(url, params=params)

    if response.status_code != 200:
        return []

    # 4. PARSE DATA
    try:
        data = response.json()
    except Exception:
        return []

    events = data.get("features", [])
    earthquakes = []

    # 5. EXTRACT DATA
    for event in events:
        props = event["properties"]
        geom = event["geometry"]

        timestamp = props["time"]

        # Case 1: timestamp is milliseconds (number)
        if isinstance(timestamp, (int, float)):
            dt = datetime.utcfromtimestamp(timestamp / 1000)
        # Case 2: timestamp is ISO string
        else:
            # removing Z to ensure format matches
            dt = datetime.fromisoformat(timestamp.replace("Z", ""))

        day = dt.strftime("%Y-%m-%d")
        time_str = dt.strftime("%H:%M:%S")

        mag = props["mag"]
        place = props["place"]
        longitude = geom["coordinates"][0]
        latitude = geom["coordinates"][1]

        quake_tuple = (day, time_str, mag, latitude, longitude, place)
        earthquakes.append(quake_tuple)

    return earthquakes
