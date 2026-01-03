import sqlite3
from datetime import datetime, timedelta
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


def query_db(K, days, min_magnitude):
    """
    Queries the database for the K strongest earthquakes within the last 'days'
    with a magnitude of at least 'min_magnitude'.
    """
    conn = sqlite3.connect('earthquakes.db')
    cursor = conn.cursor()

    # Calculate the cutoff date (current time - days)
    cutoff_date = datetime.utcnow() - timedelta(days=int(days))
    cutoff_str = cutoff_date.strftime("%Y-%m-%d")

    # SQL Query:
    # 1. Filter by magnitude and date
    # 2. Order by magnitude DESC (strongest first)
    # 3. Limit to K results
    query = """
            SELECT day, time, mag, latitude, longitude, place
            FROM earthquakes_db
            WHERE mag >= ? AND day >= ?
            ORDER BY mag DESC
                LIMIT ? \
            """

    # Execute safely using parameters
    cursor.execute(query, (float(min_magnitude), cutoff_str, int(K)))

    results = cursor.fetchall()
    conn.close()

    return results


def print_earthquakes(earthquakes):
    # 'earthquakes' è la lista di tuple restituita da query_db() [cite: 103, 106]
    for eq in earthquakes:
        # Estraiamo i dati dalla tupla in base all'ordine della query [cite: 95, 103]
        day, time, magnitude, latitude, longitude, place = eq

        # Stampiamo seguendo il formato esatto richiesto dal manuale
        print(f"day: {day}, time: {time}, magnitude: {magnitude},")
        print(f"lat: {latitude}, lon: {longitude}, place: {place}")

