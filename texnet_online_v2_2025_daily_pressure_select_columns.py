import csv
import json

# Load configuration from config.json
def load_config(config_path="config.json"):
    with open(config_path, 'r') as config_file:
        return json.load(config_file)

# Configuration
config = load_config()  # Load the configuration from config.json

# Retrieve file paths from the config file
input_file_path = config["inputcsvpath_dailybhp"]
output_file_path = config["outputcsvpath_dailybhp"]

# Define the header and the column indices to extract
header = ["UIC", "API", "wtd_ft", "bhp_m3", "date_meas"]
column_indices = [0, 1, 6, 7, 10]

try:
    with open(input_file_path, 'r') as dailypressure:
        readfile = csv.reader(dailypressure)

        with open(output_file_path, 'w', newline='') as dailypressuresimplified:
            writefile = csv.writer(dailypressuresimplified)
            # Write the defined header
            writefile.writerow(header)

            # Skip the first row (header of the original file)
            next(readfile)

            # Write the selected columns
            for row in readfile:
                try:
                    result = [row[i] for i in column_indices]
                    writefile.writerow(result)
                except IndexError as e:
                    print(f"Row processing error at row {readfile.line_num}: {e}")

except FileNotFoundError as e:
    print(f"File error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

