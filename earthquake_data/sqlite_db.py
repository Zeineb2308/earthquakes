
import sqlite3

import earthquakes

from .FetchINGV import gather_earthquakes

def create_earthquake_db(days: int, db_name: str = "earthquakes.db"):
    #Gathers earthquake data and stores it in a SQLite database.
    earthquakes = gather_earthquakes(days)
Conn = sqlite3.connect("earthquakes_db")
cursor = Conn.cursor()
cursor.execute("create table if not exist earthquakes_db"
            ("day text" , "time text" ,"mag real" , "latitude real" , "longitude real" , "place text"))
Conn.commit()
cursor.executemany(
    "insert into earthquakes_db (day, time, mag, latitude, longitude, place) "
    "values (?, ?, ?, ?, ?, ?)",
    earthquakes)
Conn.commit()
cursor.close()
Conn.close()