import sqlite3
import argparse
from datetime import datetime , timedelta

def query_db(k , days , min_magnitude , db_name ="earthquakes.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    date_threshold = datetime.now()-timedelta(days=days)
    date_str = str(date_threshold.date())
    
    sql= """
        select* from earthquakes_db
        where mag >= ? and day >= ?
        order by mag desc
        limit ?
    """
    
    cursor.execute(sql, (min_magnitude, date_str, k))
    results = cursor . fetchall()

    conn.close()
    return results


def print_earthquakes(results):
    for quake in results:
        print(f"day:{quake[0]} , time: {quake[1]} , magnitude:{quake[2]}")
        print(f"lat:{quake[3]} , lon{quake[4]} , place:{quake[5]}")
        print('_'*30)
