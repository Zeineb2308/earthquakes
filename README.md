#  Earthquake Monitor & Geospatial Analysis Tool

This software solution provides real-time monitoring of seismic events across Italy. By integrating live data from the **INGV (Istituto Nazionale di Geofisica e Vulcanologia)** with a static database of **Italian Municipalities**, the system not only reports earthquakes but adds critical context: it identifies populated areas immediately affected by the event.

The project demonstrates the application of modular software architecture, database management, and geospatial algorithms (Haversine formula) to solve a data correlation problem.

##  System Architecture & Implementation

The project is structured into modular components, ensuring maintainability. Below is a breakdown of what has been implemented:

### 1. Data  Fetching Module(`fetch_ingv.py`)
* **Functionality:** This module acts as the gateway to external data. It connects to the INGV public API to retrieve the most recent seismic events.
* **Logic:** It filters the data using a geographic bounding box that covers Italy, so only earthquakes from this area are processed.

### 2. Database Handling Module (`db_handler.py`)
* **Functionality:** We implemented a local SQLite database to store earthquake history.
* **Logic:**
    * **Duplicate Prevention:** The system checks if an event ID already exists before saving, preventing data redundancy.
    * **Data Integrity:** A "Clean Start" protocol is implemented to refresh the database during specific test runs, ensuring the analysis is always performed on the current session's data.

### 3. Distance Calculation Module (`nearby_municipalities.py`)
* **Functionality:**  It calculates the physical distance between the earthquake's epicenter and thousands of Italian cities.
* **Logic:**
    * It utilizes the **Haversine Formula**, a mathematical algorithm used in navigation, to calculate the great-circle distance between two points on a sphere (the Earth) given their longitudes and latitudes.
    * It filters results to show only cities within a specific radius (e.g., 20km), prioritizing the most impacted areas.

### 4. Main Program (`main.py`)
* **Functionality:** The central hub that orchestrates the workflow.
* **Logic:** It manages the sequence of operations: `Fetch Data` -> `Store in DB` -> `Load Municipalities` -> `Calculate Distances` -> `Display Report`.


## Installation & Operation

### 1. Environment Setup

Ensure Python 3 is installed. Install the necessary dependencies:
```bash
pip install -r requirements.txt
``` 
### 2. Data Setup

Ensure your static municipalities dataset (e.g., municipalities.csv or .db) is located in the root directory (or data/ folder). This file is required for the system to map GPS coordinates to city names.

### 3. Running the Program

The application is executed from the command line using Python.  
The user must provide three required arguments to run the program.

```bash
python main.py --days <N> --K <K> --magnitude <M>
``` 
#### Arguments Explained

| Argument | Description | Example |
| :--- | :--- | :--- |
| `--days <N>` | The number of past days to fetch data for. | `7` (Last 7 days) |
| `--K <K>` | The search radius (in km) to find nearby cities. | `20` (Within 20km) |
| `--magnitude <M>` | The minimum magnitude threshold to report. | `2.5` (Only events > 2.5) |


## Sample Output

When executed, the program will generate a report similar to the following:

```text
[INFO] Fetching seismic data from INGV (Last 7 days)...
[INFO] Found 12 events matching criteria.

------------------------------------------------
Event ID: 123456 | Magnitude: 3.2
Location: 42.1N, 13.5E | Depth: 10km
Time: 2023-10-25 14:30:00

Nearby Municipalities (within 20km):
1. Amatrice (RI) - 4.2 km away
2. Accumoli (RI) - 6.8 km away
3. Cittareale (RI) - 12.1 km away
------------------------------------------------
```

## Conclusion

This project demonstrates how earthquake data can be collected, stored, and analyzed using a modular Python application. By combining external seismic data with geographic information about Italian municipalities, the program provides meaningful insights into the potential impact of earthquakes.








