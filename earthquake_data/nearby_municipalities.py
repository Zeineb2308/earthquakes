import math
import csv
import os

def calculate_distance(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    R = 6371.0

    # Convert degrees to radians
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * \
        math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

def get_closest_municipalities(eq_lat, eq_lon):
        distances = []

        # This finds the exact folder where this script is located
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # This joins that folder path with your filename
        csv_path = os.path.join(current_dir, 'italian_municipalities.csv')

        with open(csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # IMPORTANT: Check these keys match your CSV headers exactly!
                town_name = row['comune']
                town_lat = float(row['lat'])
                town_lon = float(row['long'])

                dist = calculate_distance(eq_lat, eq_lon, town_lat, town_lon)
                distances.append((town_name, dist))

        distances.sort(key=lambda x: x[1])
        return distances[:5]

