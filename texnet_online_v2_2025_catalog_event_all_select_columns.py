import csv
import json
from datetime import datetime

# Load configuration from config.json
def load_config(config_path="config.json"):
    with open(config_path, 'r') as config_file:
        return json.load(config_file)

# Configuration
config = load_config()  # Load the configuration from config.json
date_id = datetime.today().strftime('%Y%m%d')

# File paths from the config file
input_file = config["inputcsvpath_event"]
output_file = config["outputcsvpath_event"]

def get_quarter(month):
    """Determine the quarter based on the month."""
    if month < 4:
        return "Q1"
    elif month < 7:
        return "Q2"
    elif month < 10:
        return "Q3"
    else:
        return "Q4"

def process_row(row, date_id):
    """Process a single row of data."""
    if len(row) < 8:  # Ensure there are enough columns (adjusted for latitude and longitude)
        print(f"Skipping row due to insufficient columns: {len(row)}")
        return None

    try:
        event_id = row[0]
        orig_date = row[2]
        orig_time = row[3]
        local_mag = row[4]
        latitude = row[6]
        longitude = row[8]
        depth_km_msl = row[10]

        # Parse the date
        date_obj = datetime.strptime(orig_date, '%Y-%m-%d')  # Corrected date format
        year = date_obj.year
        month = date_obj.month
        quarter = get_quarter(month)

    except ValueError as e:
        print(f"Error parsing date: {e} - Row: {row}")
        return None

    # Prepare the result row
    result = [event_id, orig_date, orig_time, local_mag, latitude, longitude, depth_km_msl]
    result.extend([f"{year} {quarter}", month, year, date_id])
    return result

# Main processing
with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    header_written = False
    for i, row in enumerate(reader):
        print(f"Processing row {i}")  # Debugging line
        if i == 0:
            # Write the header row
            writer.writerow([
                "eventid", "origindate", "origintime", "localmag",
                "latitude", "longitude", "depth_km_msl", # New headers for latitude and longitude
                "quartyear", "eventmonth", "eventyear", "pyrundate"
            ])
            header_written = True
        else:
            processed_row = process_row(row, date_id)
            if processed_row:
                writer.writerow(processed_row)

    if not header_written:
        print("No header written, check the input file format.")
