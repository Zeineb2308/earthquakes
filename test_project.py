"""
Test Suite for Earthquake Software.

Run this file to verify the correctness of the implementation.
"""
import unittest
import csv
import sqlite3
import os
from earthquake_data.db_handler import query_db, create_earthquake_db


class TestProject(unittest.TestCase):
    """
    Implements tests required by the Project Manual (Step 7).
    """

    @classmethod
    def setUpClass(cls):
        """
        Ensure the database exists and is populated before running tests.
        """
        if not os.path.exists('earthquakes.db'):
            # Create a sample DB if it doesn't exist
            create_earthquake_db(days=30)

    def test_bounding_box(self):
        """
        Test 1: Check if key Italian cities fall in the bounding box.

        Cities checked: Padova, Palermo, Parma.
        """
        cities = {
            "Padova": (45.4064, 11.8768),
            "Palermo": (38.1157, 13.3615),
            "Parma": (44.8015, 10.3279)
        }

        bbox = {}
        # Path handling to find the CSV
        if os.path.exists('earthquake_data/bounding_box.csv'):
            path = 'earthquake_data/bounding_box.csv'
        elif os.path.exists('earthquake_app/bounding_box.csv'):
            path = 'earthquake_app/bounding_box.csv'
        else:
            self.fail(
                "bounding_box.csv not found. "
                "Run write_bounding_box.py."
            )
            return

        with open(path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                bbox[row['key']] = float(row['value'])

        for city, (lat, lon) in cities.items():
            with self.subTest(city=city):
                self.assertGreaterEqual(lat, bbox['minlatitude'])
                self.assertLessEqual(lat, bbox['maxlatitude'])
                self.assertGreaterEqual(lon, bbox['minlongitude'])
                self.assertLessEqual(lon, bbox['maxlongitude'])

    def test_magnitude(self):
        """
        Test 2: Check that there are no impossible earthquakes (> 9.5).
        """
        conn = sqlite3.connect('earthquakes.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM earthquakes_db WHERE mag > 9.5")
        results = cursor.fetchall()
        conn.close()
        self.assertEqual(len(results), 0, "Found impossible earthquake > 9.5!")

    def test_order(self):
        """
        Test 3: Check that query_db returns results sorted by magnitude.
        """
        results = query_db(K=10, days=365, min_magnitude=0.0)

        if len(results) < 2:
            self.skipTest("Not enough data in DB to test sorting.")

        for i in range(len(results) - 1):
            mag_curr = results[i][2]
            mag_next = results[i + 1][2]
            self.assertGreaterEqual(
                mag_curr, mag_next, "Results are not sorted!"
            )

    def test_impossible_magnitude(self):
        """
        Test 4: Verifies that asking for Magnitude 10.0 returns empty.
        """
        results = query_db(10, 30, 10.0)
        self.assertEqual(
            len(results), 0,
            "Querying for magnitude 10.0 should return no results."
        )


if __name__ == '__main__':
    unittest.main()
