"""
Add-on Module: Nearby Municipalities.

Calculates the distance between earthquake epicenters and Italian municipalities.
"""
import csv
import os
import math


def load_municipalities():
    """
    Loads city data from the CSV file. It runs just once at the start to keep the program fast.
    """
    municipalities = []

    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, 'italian_municipalities.csv')

    if not os.path.exists(csv_path):
        return []

    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                municipalities.append({
                    'name': row['name'],
                    'lat': float(row['latitude']),
                    'lon': float(row['longitude'])
                })
            except (ValueError, KeyError):
                continue
    return municipalities


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculates the great-circle distance between two points on the Earth surface.

    Returns:
        float: Distance in kilometers.
    """
    R = 6371.0  # Earth radius in km
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)

    a = (math.sin(d_lat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(d_lon / 2) ** 2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def get_closest_municipalities(eq_lat, eq_lon, municipalities, n=5):
    """
    Finds the 'n' municipalities closest to the given coordinates.
    """
    distances = []
    for city in municipalities:
        dist = haversine_distance(eq_lat, eq_lon, city['lat'], city['lon'])
        distances.append((city['name'], dist))

    # Sorting by distance (ascending)
    distances.sort(key=lambda x: x[1])
    return distances[:n]