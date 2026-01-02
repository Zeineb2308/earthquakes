import sqlite3
from .FetchINGV import gather_earthquakes


def create_earthquake_db(days):
    # 1. Fetch data using the function you made in Point 4
    # This calls gather_earthquakes and stores the result in 'earthquakes'
    earthquakes = gather_earthquakes(days)

    # 2. Open a connection and a cursor to the database 'earthquakes.db'
    conn = sqlite3.connect('earthquakes.db')
    cursor = conn.cursor()

    # 3. Create the table 'earthquakes_db' if it doesn't exist
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

    # Execute the creation statement and commit
    cursor.execute(create_table_sql)
    conn.commit()

    # 4. Insert all earthquakes into the database
    # We use executemany to insert the list of tuples efficiently
    insert_sql = "INSERT INTO earthquakes_db (day, time, mag, latitude, longitude, place) VALUES (?, ?, ?, ?, ?, ?)"
    cursor.executemany(insert_sql, earthquakes)

    # 5. Close the connection
    conn.commit()
    conn.close()