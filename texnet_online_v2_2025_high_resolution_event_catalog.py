import csv
import datetime
import json

# Load configuration from config.json
def load_config(config_path="config.json"):
    with open(config_path, 'r') as config_file:
        return json.load(config_file)

# Configuration
config = load_config()  # Load the configuration from config.json

# Retrieve file paths from the config file
input_file = config["inputcsvpath_hires"]
output_file = config["outputcsvpath_hires"]

def create_date(day, month, year):
    """Create a date object from day, month, and year, handling invalid dates."""
    try:
        return datetime.date(year, month, day).isoformat()  # Return in ISO format for consistency
    except ValueError as e:
        print(f"Invalid date: {day}-{month}-{year} ({e})")
        return None

# Open and process the input and output files
with open(input_file, 'r') as texnethires:
    readfile = csv.reader(texnethires)
    
    with open(output_file, 'w', newline='') as texnethiresplus:
        writefile = csv.writer(texnethiresplus)
        
        for i, row in enumerate(readfile):
            if i == 0:
                # Write header
                writefile.writerow(["eventid", "eventdate", "year", "month","day", "lat_reloc", "lon_reloc", "depth_reloc", "magnitude", "cat_lat", "cat_lon", "cat_depth"])
            else:
                # Process each row
                try:
                    day = int(row[4])
                    month = int(row[3])
                    year = int(row[2])
                    eventdate = create_date(day, month, year)

                    # Prepare result row
                    result = [row[1], eventdate, row[2], row[3], row[4], row[9], row[10], row[11], row[12], row[24], row[25], row[26]]
                    writefile.writerow(result)
                except (IndexError, ValueError) as e:
                    print(f"Error processing row {i}: {e}")

