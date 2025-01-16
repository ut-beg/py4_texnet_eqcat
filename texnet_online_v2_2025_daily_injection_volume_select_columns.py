import csv
import json

# Load configuration from config.json
def load_config(config_path="config.json"):
    with open(config_path, 'r') as config_file:
        return json.load(config_file)

# Configuration
config = load_config()  # Load the configuration from config.json

# Retrieve file paths from the config file
INPUT_FILE_PATH = config["inputcsvpath_dailyinj"]
OUTPUT_FILE_PATH = config["outputcsvpath_dailyinj"]

# Define the header and the column indices to extract
HEADER = [
    "UIC", "API", "inj_date", "vol_bbls", "cmpl_top", "cmpl_bot",
    "UIC_type", "wtd_ft", "slon", "slat"
]
COLUMN_INDICES = [0, 1, 6, 7, 11, 12, 20, 29, 15, 16]

def process_csv(input_path, output_path):
    try:
        with open(input_path, 'r') as dailyvolume:
            readfile = csv.reader(dailyvolume)
            with open(output_path, 'w', newline='') as dailyvolumesimplified:
                writefile = csv.writer(dailyvolumesimplified)
                
                # Write the defined header
                writefile.writerow(HEADER)

                # Skip the original header
                next(readfile)

                # Write the selected columns
                for line_number, row in enumerate(readfile, start=2):  # start=2 to account for header
                    try:
                        result = [row[i] for i in COLUMN_INDICES]
                        writefile.writerow(result)
                    except IndexError as e:
                        print(f"Row processing error at row {line_number}: {e}")

    except FileNotFoundError as e:
        print(f"File error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Call the function
process_csv(INPUT_FILE_PATH, OUTPUT_FILE_PATH)

