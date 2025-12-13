import sqlite3
from FetchINGV import gather_earthquakes

def create_earthquake_db(days: int, db_name: str = "earthquakes.db"):
    # Gathers earthquake data and stores it in a SQLite database.
    earthquakes = gather_earthquakes(days)

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS earthquakes_db (
            day TEXT,
            time TEXT,
            mag REAL,
            latitude REAL,
            longitude REAL,
            place TEXT
        )
    """)

    conn.commit()

    cursor.executemany(
        "INSERT INTO earthquakes_db (day, time, mag, latitude, longitude, place) VALUES (?, ?, ?, ?, ?, ?)",
        earthquakes
    )

    conn.commit()
    cursor.close()
    conn.close()
