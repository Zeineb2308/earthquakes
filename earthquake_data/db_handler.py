"""
Database Handler Module.

Manages the local SQLite database to store and retrieve earthquake data.
"""
import sqlite3
from datetime import datetime, timedelta
from earthquake_data.fetch_ingv import gather_earthquakes


def create_earthquake_db(days):
    """
    Fetch fresh data and update the local database.

    IMPORTANT: This function clears (DELETE) old data to prevent duplicates.

    Args:
        days (int): Number of days to fetch.
    """
    earthquakes = gather_earthquakes(days)

    # Opening a connection and a cursor to the database 'earthquakes.db'
    conn = sqlite3.connect('earthquakes.db')
    cursor = conn.cursor()

    # Create the table 'earthquakes_db' if it doesn't exist
    # The columns must be: day, time, mag, latitude, longitude, place
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS earthquakes_db (
        day TEXT,
        time TEXT,
        mag REAL,
        latitude REAL,
        longitude REAL,
        place TEXT
    );
    """

    cursor.execute(create_table_sql)

    # FIX: clear old data before inserting new data
    cursor.execute("DELETE FROM earthquakes_db")

    # Insert all earthquakes into the database
    insert_sql = """
        INSERT INTO earthquakes_db
        (day, time, mag, latitude, longitude, place)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    cursor.executemany(insert_sql, earthquakes)

    # 5. Close the connection
    conn.commit()
    conn.close()


def query_db(K, days, min_magnitude):
    """
    Query the database for the top K strongest earthquakes.

    Args:
        K (int): Max number of results.
        days (int): Time range in days.
        min_magnitude (float): Minimum magnitude threshold.

    Returns:
        list: Filtered and sorted list of earthquakes.
    """
    conn = sqlite3.connect('earthquakes.db')
    cursor = conn.cursor()

    cutoff_date = datetime.utcnow() - timedelta(days=days)
    cutoff_str = cutoff_date.strftime("%Y-%m-%d")

    query = """
            SELECT day, time, mag, latitude, longitude, place
            FROM earthquakes_db
            WHERE mag >= ? AND day >= ?
            ORDER BY mag DESC
            LIMIT ?
            """

    cursor.execute(query, (min_magnitude, cutoff_str, K))
    results = cursor.fetchall()
    conn.close()
    return results
