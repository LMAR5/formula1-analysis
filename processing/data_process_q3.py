from pathlib import Path
import pandas as pd

# 1. Load data initial Dataframes directly from CSV files
app_dir = Path(__file__).parent.parent

## Load your CSV files here, follow the example in "data_process_sidebar.py"

str_data_path = str(app_dir) + '\\data\\'


file_paths = {
    "pit_stop_records": "Pit_Stop_Records.csv",
    "race_results": "Race_Results.csv",
    "lap_timings": "Lap_Timings.csv",
    "race_schedule": "Race_Schedule.csv",
    "track_information": "Track_Information.csv"
}

# Read each relevant CSV file into a pandas DataFrame
dataframes = {name: pd.read_csv(str_data_path + file_name) for name, file_name in file_paths.items()}


pit_stop_records = dataframes["pit_stop_records"]
race_results = dataframes["race_results"]
lap_timings = dataframes["lap_timings"]
race_schedule = dataframes["race_schedule"]
track_information = dataframes["track_information"]

'''
for name, df in dataframes.items():
    print(f"Loaded dataset: {name}")
    print(df.head(), "\n")
'''

# 2. Create dictionaries, arrays, Dataframes, or whichever DS you need for your charts to export them

## Create the data structures (DS) you need to manage your data for your plots, follow the example in "data_process_sidebar.py"


