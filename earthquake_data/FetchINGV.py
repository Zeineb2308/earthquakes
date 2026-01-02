import os
import csv
import requests
from datetime import datetime , timedelta

def gather_earthquakes(days):
    bounding_box =  {}
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CSV_PATH = os.path.join(BASE_DIR, "..","..","..","bounding_box.csv")
    with open(CSV_PATH, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            key = row["key"]
            value = float (row["value"])
            bounding_box[key] = value


    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=days)
    url = "https://webservices.ingv.it/fdsnws/event/1/query"
    params= {
        "format": "geojson",
        "starttime": str(start_time.date()),
        "endtime": str(end_time.date()),
        "minlatitude": bounding_box["minlatitude"],
        "maxlatitude": bounding_box["maxlatitude"],
        "minlongitude": bounding_box["minlongitude"],
        "maxlongitude": bounding_box["maxlongitude"],
    }

    response = requests.get(url, params=params)
    print("Status code:", response.status_code)
    print("Response preview:", response.text[:200])

    data = response.json()
    events = data["features"]
    earthquake = []
    for event in events:
        props = event['properties']
        geom = event['geometry']

        timestamp_ms = props["time"]                 
        dt = datetime.utcfromtimestamp(timestamp_ms / 1000.0) 
        day = str(dt.date())
        time_str = str(dt.time()).split(".")[0]

        mag = props["mag"]
        place = props["place"]
        longitude = geom["coordinates"][0]
        latitude = geom["coordinates"][1]

        quake_tuple = ( day , time_str , mag , latitude , longitude , place)
        earthquake.append(quake_tuple)
    return earthquake
