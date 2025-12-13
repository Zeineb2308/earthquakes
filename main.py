import argparse
from sqlite_db import create_earthquake_db
from query_db import query_db , print_earthquakes
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int)
    parser.add_argument("--k" , type=int)
    parser.add_argument("--magnitude" , type=float)
    
    args = parser.parse_args
    create_earthquake_db(args.days)
    results = query_db(args.k ,args.days , args.magnitude)
    print_earthquakes(results)
if __name__ == "__main__":
    main()