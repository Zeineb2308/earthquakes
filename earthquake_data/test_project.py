import unittest
import csv
import sqlite3
import os
import sys


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from main import query_db, create_earthquake_db


class TestProject(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Ensure the database exists before running tests."""
        if not os.path.exists('earthquakes.db'):
            create_earthquake_db(30)

    def test_bounding_box(self):
        """
        Test 1: Check if Padova, Palermo, and Parma are in the bounding box.
        """
        bbox = {}


        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)

        possible_paths = [
            os.path.join(project_root, 'bounding_box.csv'),
            os.path.join(current_dir, 'bounding_box.csv'),
            'bounding_box.csv'
        ]

        csv_path = None
        for path in possible_paths:
            if os.path.exists(path):
                csv_path = path
                break

        if csv_path is None:
            self.fail("Could not find 'bounding_box.csv'.")

        # Open and read the file
        with open(csv_path, mode='r') as infile:
            reader = csv.reader(infile)
            for row in reader:
                if row and len(row) >= 2:
                    try:
                        val = float(row[1])
                        bbox[row[0]] = val
                    except ValueError:
                        continue

        cities = {
            "Padova": (45.406, 11.876),
            "Palermo": (38.115, 13.361),
            "Parma": (44.801, 10.327)
        }


        if not bbox:
            self.fail("CSV file was found but no valid numeric data could be read from it.")

        for city, (lat, lon) in cities.items():
            with self.subTest(city=city):
                self.assertGreaterEqual(lat, bbox.get('minlatitude', -90))
                self.assertLessEqual(lat, bbox.get('maxlatitude', 90))
                self.assertGreaterEqual(lon, bbox.get('minlongitude', -180))
                self.assertLessEqual(lon, bbox.get('maxlongitude', 180))

    def test_magnitude(self):
        """Test 2: Check that no earthquake has magnitude > 9.5."""
        db_path = 'earthquakes.db'
        if not os.path.exists(db_path):
            db_path = os.path.join('..', 'earthquakes.db')

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM earthquakes_db WHERE mag > 9.5")
        results = cursor.fetchall()
        self.assertEqual(len(results), 0, "Found an earthquake with magnitude > 9.5, which is impossible.")
        conn.close()

    def test_order(self):
        """Test 3: Check if query_db returns a list sorted decreasingly by magnitude."""
        results = query_db(10, 365, 2.0)
        for i in range(len(results) - 1):
            current_mag = results[i][2]
            next_mag = results[i + 1][2]
            self.assertGreaterEqual(current_mag, next_mag,
                                    f"List is not sorted: {current_mag} is not >= {next_mag}")

    def test_impossible_magnitude(self):
        """Test 4: Verifies that asking for Magnitude 10.0 returns empty."""
        results = query_db(10, 30, 10.0)
        self.assertEqual(len(results), 0, "Querying for magnitude 10.0 should return no results.")


if __name__ == '__main__':
    unittest