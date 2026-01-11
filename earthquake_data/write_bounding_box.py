import csv

def create_bounding_box_csv():
    """
    Creates a CSV file named 'bounding_box.csv' containing geographic coordinates.

    This function defines a dictionary with the limits of the Italian region
    (min/max latitude and longitude) and writes it to a CSV file.
    This allows other parts of the program to read the configuration dynamically.
    """
    # Define the dictionary as required by the Project Manual
    bounding_box = {
        'minlatitude': 35.0,
        'maxlatitude': 47.5,
        'minlongitude': 5.0,
        'maxlongitude': 20.0
    }

    # Open the file in write mode ('w')
    # newline='' is used to prevent empty lines between rows on Windows
    with open('bounding_box.csv', mode='w', newline='') as csv_file:
        # Create a CSV writer object
        writer = csv.DictWriter(csv_file, fieldnames=["key", "value"])

        # Write the header row (key, value)
        writer.writeheader()

        # Iterate through the dictionary and write each pair as a row
        for key, value in bounding_box.items():
            writer.writerow({'key': key, 'value': value})

    print("File 'bounding_box.csv' created successfully.")

# Execute the function only if run as a script
if __name__ == "__main__":
    create_bounding_box_csv()