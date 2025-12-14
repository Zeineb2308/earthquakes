import argparse

def main():
    #Step 1: Initialize the parser, which will read the command line inputs
    parser = argparse.ArgumentParser(description="Earthquake search tool")

    #Step 2: Add the arguments days,K and magnitude with Help
    #as per instructions required=True and each argument start's with --
    #Argument 1: days (integer) -> if 30, it searches up to 30 days ago.
    parser.add_argument("--days",
                        type=int,
                        required=True,
                        help="Number of days to search going backwards, e.g. last 30 days")

    #Argument 2: K (integer) -> if 3 gives the 3 strongest earthquakes within magnitude parameters
    parser.add_argument("--K",
                        type=int,
                        required=True,
                        help="Number of strongest earthquakes, e.g. top 3 if K=3")

    #Argument 3: magnitude (float) -> gives the minimum magnitude allowed
    parser.add_argument("--magnitude",
                        type=float,
                        required=True,
                        help="Minimum strength of the earthquakes allowed , e.g. if 2.5 then the code gets only earthquakes stronger than 2.5 mag.")

    """
    Step 3: Parse the arguments
    This line checks if the user wrote the commands/input correctly
    If not all the right commands are inserted then it gives and error
    The error message should be: "the following arguments are required: --days, --K, --magnitude"
    """
    args = parser.parse_args()

    #Step 4: print the values to verify the code works
    print(f"Searching for the strongest {args.K} earthquakes")
    print(f"Over the last {args.days} days")
    print(f"With a magnitude of at least {args.magnitude}")

#Step 5: ensure that the code works only when run directly
if __name__ == "__main__":
    main()

#step 3 is verified to work (python main.py)
#step 4 is verified to work (python main.py --days 30 --K 5 --magnitude 2.5)
#Help message has been tested and it works as intended (python main.py --help)