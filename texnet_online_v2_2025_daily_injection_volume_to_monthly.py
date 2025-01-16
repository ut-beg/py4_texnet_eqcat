import csv
import os
import json
from datetime import datetime

# Load configuration from config.json
def load_config(config_path="config.json"):
    with open(config_path, 'r') as config_file:
        return json.load(config_file)

# Configuration
config = load_config()  # Load the configuration from config.json

# Retrieve file paths from the config file
RAW_INPUT_FILE = config["inputcsvpath_sum_daily"]
INTERMEDIATE_CSV_FILE = config["intermediate_sum_daily_file"]
OUTPUT_FILE = config["outputcsvpath_sum_daily"]

# Step 1: Process and simplify the initial CSV file
def simplify_csv(input_file, output_file):
    with open(input_file, 'r') as dailyvolumetable:
        reader = csv.reader(dailyvolumetable)
        with open(output_file, 'w', newline='') as dailyvolumeselectcolumns:
            writer = csv.writer(dailyvolumeselectcolumns)
            for i, row in enumerate(reader):
                try:
                    if i == 0:
                        writer.writerow(["UIC", "API", "lon_wgs84", "lat_wgs84", "UIC_type", 
                                         "cmpl_top", "cmpl_bot", "inj_date", "vol_bbls", 
                                         "wtd_ft"])
                    else:
                        result = [row[0], row[1], row[15], row[16], row[20],
                                  row[11], row[12], row[6], row[7], row[29]]
                        writer.writerow(result)
                except Exception as e:
                    print(f"ERROR: {e}")

# Step 2: Get month-year strings for processing
def get_month_year_strings(start_year, end_year, end_month):
    month_year_strings = []
    for year in range(start_year, end_year + 1):
        start_month = 1 if year > start_year else 1
        end_month = end_month if year == end_year else 12
        for month in range(start_month, end_month + 1):
            month_year_strings.append(f"{month:02d}/{year}")
    return month_year_strings

# Step 3: Process CSV to calculate monthly volumes
def process_csv(input_file, month_year_strings):
    well_data = {}
    
    with open(input_file, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)
        
        for i, row in enumerate(reader):
            if i % 10 == 0:
                print(f"Processing row {i}")
                
            api = row[1]
            uic = row[0]
            lon_wgs84 = row[2]
            lat_wgs84 = row[3]
            inj_date = row[7]
            typeuic = row[4]
            cinjtop = row[5]
            cinjbot = row[6]
            totwelldp = row[9]
            try:
                vol_bbls = float(row[8])
            except ValueError:
                print(f"Skipping invalid volume: {row[8]}")
                continue

            try:
                year, month, day = map(int, inj_date.split('-'))
                month_year = f"{month:02d}/{year}"
            except ValueError:
                print(f"Skipping invalid date format: {inj_date}")
                continue
            
            if api not in well_data:
                well_data[api] = {
                    'UIC': uic,
                    'lon_wgs84': lon_wgs84,
                    'lat_wgs84': lat_wgs84,
                    'UIC_type': typeuic,
                    'cmpl_top': cinjtop,
                    'cmpl_bot': cinjbot,
                    'wtd_ft': totwelldp,
                    **{f"{date}_bbls": 0 for date in month_year_strings}
                }
            
            # Add volume to the correct month-year
            if f"{month_year}_bbls" in well_data[api]:
                well_data[api][f"{month_year}_bbls"] += vol_bbls
                
    return well_data

# Step 4: Write output CSV
def write_output_csv(output_file, well_data, month_year_strings):
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        header = ['UIC', 'API', 'lon_wgs84', 'lat_wgs84', 'injectdate', 'suminjbbls','UIC_type', 'cmpl_top','cmpl_bot', 'wtd_ft']
        writer.writerow(header)
        
        for api, data in well_data.items():
            uic = data.pop('UIC')
            lon_wgs84 = data.pop('lon_wgs84')
            lat_wgs84 = data.pop('lat_wgs84')
            typeuic = data.pop('UIC_type')
            cinjtop = data.pop('cmpl_top')
            cinjbot = data.pop('cmpl_bot')
            totwelldp = data.pop('wtd_ft')
            for month_year in month_year_strings:
                key = f"{month_year}_bbls"
                value = data.get(key, 0)
                if value > 0:
                    month, year = month_year.split('/')
                    result_date = f"{month}/01/{year}"  # Assuming the first day of the month
                    row = [uic, api, lon_wgs84, lat_wgs84, result_date, value, typeuic, cinjtop, cinjbot, totwelldp]
                    writer.writerow(row)

# Main Processing
start_year = 2016
current_year = datetime.now().year
current_month = datetime.now().month
month_year_strings = get_month_year_strings(start_year, current_year, current_month)

# Step 1: Simplify the initial CSV file
simplify_csv(RAW_INPUT_FILE, INTERMEDIATE_CSV_FILE)

# Step 2: Process the simplified CSV file and write the summary
well_data = process_csv(INTERMEDIATE_CSV_FILE, month_year_strings)
print(f"Unique wells in spreadsheet = {len(well_data)}")
write_output_csv(OUTPUT_FILE, well_data, month_year_strings)

print("Processing complete.")

try:
    os.remove(INTERMEDIATE_CSV_FILE)
    print(f"Intermediate file {INTERMEDIATE_CSV_FILE} has been removed.")
except OSError as e:
    print(f"Error removing intermediate file: {e}")
