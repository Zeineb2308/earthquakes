import requests
import datetime
import json


USGS_URL = 'https://earthquake.usgs.gov/fdsnws/event/1/query?starttime={}&format=geojson&limit=20000'

def get_earthquake(days_past):
    """
    Fetches the list of earthquakes registered in the last 'days_past' days around the world
    and returns the one with the highest magnitude.

    :param days_past: The number of days in the past to search for earthquakes.
    :return: A tuple containing the magnitude and the place of the largest earthquake.
    """
    #get the date of today - days_past days at 00 AM
    start_date = (datetime.datetime.now() + datetime.timedelta(days=-days_past)).strftime("%Y-%m-%d")
    url = USGS_URL.format(start_date)
    r = requests.get(url)
    events = json.loads(requests.get(url).text)
    magnitude = 0
    place = ''
    for event in events['features']:
        try:
            mag = float(event['properties']['mag'])
        except TypeError:
            pass
        if mag > magnitude:
            magnitude = mag
            place = event['properties']['place']
    return magnitude, place