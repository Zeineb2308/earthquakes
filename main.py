import argparse

from earthquake_data.db_handler import create_earthquake_db, query_db, print_earthquakes

def main():
    # Step 1: Initialize the parser
    parser = argparse.ArgumentParser(description="Earthquake search tool")

    # Step 2: Add all arguments (Standard + Add-on)
    parser.add_argument("--days",
                        type=int,
                        required=True,
                        help="Number of days to search going backwards, e.g. last 30 days")

    parser.add_argument("--K",
                        type=int,
                        required=True,
                        help="Number of strongest earthquakes, e.g. top 3 if K=3")

    parser.add_argument("--magnitude",
                        type=float,
                        required=True,
                        help="Minimum strength of the earthquakes allowed")

    # Add-on: Finding 5 closest municipalities
    parser.add_argument('--show-closest',
                        action='store_true',
                        help="Show the 5 closest municipalities for each earthquake")

    # Step 3: Parse all arguments at once
    args = parser.parse_args()

    # Step 4:
    # 1. Gather data and create/update the database [cite: 91, 102]
    create_earthquake_db(args.days)

    # 2. Query the database for the strongest earthquakes [cite: 102, 103]
    earthquakes = query_db(args.K, args.days, args.magnitude)

    # 3. Print the results [cite: 103, 137, 139]
    print_earthquakes(earthquakes, show_closest=args.show_closest)

    # Verification prints
    print(f"\n--- Search Summary ---")
    print(f"Strongest {args.K} earthquakes")
    print(f"Timeframe: Last {args.days} days")
    print(f"Minimum Magnitude: {args.magnitude}")
    if args.show_closest:
        print("Add-on: Show closest municipalities is ENABLED")


# Step 5: Ensure the code works only when run directly
if __name__ == "__main__":
    main()

