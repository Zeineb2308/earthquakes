"""
Earthquake Search Tool (INGV) - Main Module.

This is the main part of our software that links everything together.
It handles grabbing the earthquake data, updating our database,
and letting users run searches.

It includes an extra feature that can find the closest
towns to each earthquake epicenter.
"""

import argparse
from earthquake_data.db_handler import create_earthquake_db, query_db
from earthquake_data.nearby_municipalities import (
    load_municipalities,
    get_closest_municipalities
)


def print_earthquakes(earthquakes, show_closest, municipalities_data):
    """
    Print the list of earthquakes to the console.

    Args:
        earthquakes (list): List of tuples containing earthquake data.
        show_closest (bool): Flag to enable/disable the add-on output.
        municipalities_data (list): Pre-loaded municipality data for add-on.
    """
    if not earthquakes:
        print("No earthquakes found matching the criteria.")
        return

    for eq in earthquakes:
        day, time, mag, lat, lon, place = eq

        print("-" * 50)
        print(f"day: {day}, time: {time}, magnitude: {mag},")
        print(f"lat: {lat}, lon: {lon}, place: {place}")

        if show_closest and municipalities_data:
            # Calculating distance using the pre-loaded data
            closest = get_closest_municipalities(
                lat, lon, municipalities_data
            )
            print("   >>> Closest Municipalities (Add-on):")
            for name, dist in closest:
                print(f"       * {name}: {dist:.2f} km")


def main():
    """
    Execute the main program.

    Parse arguments, initializes the database, and displays results.
    """
    parser = argparse.ArgumentParser(
        description="Search for the strongest earthquakes in Italy"
    )

    # Add all arguments (Standard + Add-on)
    parser.add_argument("--days",
                        type=int,
                        required=True,
                        help="Number of days to search going backwards")

    parser.add_argument("--K",
                        type=int,
                        required=True,
                        help="Number of strongest earthquakes")

    parser.add_argument("--magnitude",
                        type=float,
                        required=True,
                        help="Minimum strength of the earthquakes allowed")

    # Add-on: Finding 5 closest municipalities
    parser.add_argument('--addon',
                        action='store_true',
                        help="Show the 5 closest municipalities for each eq")

    args = parser.parse_args()

    # Loads municipalities CSV only ONCE if add-on is active
    municipalities_data = []
    if args.addon:
        print("Loading municipalities data...")
        municipalities_data = load_municipalities()
        if not municipalities_data:
            print("WARNING: 'italian_municipalities.csv' not found. "
                  "Add-on disabled.")

    print(f"Updating database (Last {args.days} days)...")
    create_earthquake_db(args.days)

    results = query_db(args.K, args.days, args.magnitude)

    print("\n--- Search Results ---")
    print_earthquakes(results, args.addon, municipalities_data)


if __name__ == "__main__":
    main()
