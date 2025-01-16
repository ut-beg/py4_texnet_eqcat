import csv
import os
import json
from datetime import datetime

date_id = datetime.today().strftime('%Y%m%d')

# Load configuration from config.json
def load_config(config_path="config.json"):
    with open(config_path, 'r') as config_file:
        return json.load(config_file)

# Configuration
config = load_config()  # Load the configuration from config.json

# Retrieve file paths from the config file
input_station_file = config["inputcsvpath_station"]
output_station_all_file = config["outputcsvpath_station_all"]
output_station_active_file = config["outputcsvpath_station_active"]
intermediate_station_file = config["intermediate_station_file"]
intermediate_station_file2 = config["intermediate_station_file2"]
intermediate_station_file3 = config["intermediate_station_file3"]

def determine_label(network, station, enddate):
    """Determine the label for a station based on network, station code, and enddate."""
    station_prefix = station[:4] if len(station) >= 4 else station

    if enddate.strip():
        return "Decommissioned"

    if network == "TX":
        if station_prefix.startswith(("DG", "OG")):
            return "TexNet short period"
        if station_prefix.startswith(("EF", "FW", "MB", "PB", "PH", "ET01")) or \
           (station_prefix.startswith("SN") and not station_prefix.startswith("SNAG")):
            return "TexNet portable"
        if station_prefix == "SNAG":
            return "TexNet permanent"
        return "TexNet permanent"

    network_labels = {
        "2T": "TexNet portable", "4F": "TexNet portable", "4T": "TexNet portable", "ZW": "TexNet portable",
        "4O": "Private shared", "DB": "Private shared",
        "AE": "Other", "AG": "Other", "AM": "Other", "EP": "Other", "G": "Other", "GM": "Other",
        "IM": "Other", "IU": "Other", "MG": "Other", "MX": "Other", "N4": "Other", "NQ": "Other",
        "NX": "Other", "OK": "Other", "PI": "Other", "SC": "Other", "US": "Other", "ZP": "Other"
    }

    return network_labels.get(network, "Other")

def process_station_file(input_path, output_path):
    """Process the initial station file and add a label column."""
    try:
        with open(input_path, 'r') as infile, open(output_path, 'w', newline='') as outfile:
            reader = csv.reader(infile)
            writer = csv.writer(outfile)

            for i, row in enumerate(reader):
                if i == 0:
                    writer.writerow([ 
                        "network", "station", "lon_wgs84", "lat_wgs84", "affiliation", "archive", 
                        "location", "place", "elevation", "startdate", "enddate", "label"
                    ])
                else:
                    network = row[0]
                    station = row[1]
                    enddate = row[10]
                    label = determine_label(network, station, enddate)
                    row.append(label)
                    writer.writerow(row)
    except Exception as e:
        print(f"Error processing station file: {e}")

def process_intermediate_file2(input_path, output_path):
    """Process the intermediate file to add date components and quarter."""
    try:
        with open(input_path, 'r') as infile, open(output_path, 'w', newline='') as outfile:
            reader = csv.reader(infile)
            writer = csv.writer(outfile)

            for i, row in enumerate(reader):
                if i == 0:
                    writer.writerow([ 
                        "network", "station", "lon_wgs84", "lat_wgs84", "affiliation", "archive",
                        "location", "place", "elevation", "startdate", "enddate", "label",
                        "startmonth", "startyear", "startqyear", "pyrundate"
                    ])
                else:
                    startdate = row[9]
                    year, month, day = map(int, startdate.split("-"))

                    quarter = "Q1" if month < 4 else \
                              "Q2" if month < 7 else \
                              "Q3" if month < 10 else \
                              "Q4"

                    row.append(month)
                    row.append(year)
                    row.append(f"{year} {quarter}")
                    row.append(date_id)

                    writer.writerow(row)
    except Exception as e:
        print(f"Error processing final file: {e}")

def filter_active_stations(input_path, output_path):
    """Filter out decommissioned stations and write to a new CSV file excluding the enddate field."""
    try:
        with open(input_path, 'r') as infile, open(output_path, 'w', newline='') as outfile:
            reader = csv.reader(infile)
            writer = csv.writer(outfile)

            for i, row in enumerate(reader):
                if i == 0:
                    writer.writerow([ 
                        "network", "station", "lon_wgs84", "lat_wgs84", "affiliation", "archive",
                        "location", "place", "elevation", "startdate", "label",
                        "startmonth", "startyear", "startqyear", "pyrundate"
                    ])
                else:
                    label = row[11]  # Assuming 'label' is the 12th column (index 11)
                    if label != "Decommissioned":
                        row.pop(10)  # Exclude 'enddate' (index 10)
                        writer.writerow(row)
    except Exception as e:
        print(f"Error filtering active stations: {e}")

def remove_column(input_path, output_path, col_index):
    """Remove a specified column from the CSV file."""
    try:
        with open(input_path, 'r') as infile, open(output_path, 'w', newline='') as outfile:
            reader = csv.reader(infile)
            writer = csv.writer(outfile)

            for i, row in enumerate(reader):
                if i == 0:
                    # Write header without the specified column
                    new_header = [col for j, col in enumerate(row) if j != col_index]
                    writer.writerow(new_header)
                else:
                    # Write row without the specified column
                    new_row = [col for j, col in enumerate(row) if j != col_index]
                    writer.writerow(new_row)
    except Exception as e:
        print(f"Error removing column from file: {e}")

# Process the initial and final files
process_station_file(input_station_file, intermediate_station_file)
process_intermediate_file2(intermediate_station_file, intermediate_station_file2)

# Filter out decommissioned stations
filter_active_stations(intermediate_station_file2, intermediate_station_file3)

# Remove the 7th column (index 6) from intermediate files
remove_column(intermediate_station_file2, output_station_all_file, 6)
remove_column(intermediate_station_file3, output_station_active_file, 6)

# Remove the intermediate files
try:
    os.remove(intermediate_station_file)
    os.remove(intermediate_station_file2)
    os.remove(intermediate_station_file3)
except Exception as e:
    print(f"Error removing intermediate files: {e}")
