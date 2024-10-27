from pathlib import Path
import pandas as pd

# 1. Load data initial Dataframes directly from CSV files
app_dir = Path(__file__).parent.parent
race_schedule_df = pd.read_csv(app_dir / "data/Race_Schedule.csv").sort_values(by='year')

## Load your CSV files here, follow the example in "data_process_sidebar.py"



# 2. Create dictionaries, arrays, Dataframes, or whichever DS you need for your charts to export them

## Create the data structures (DS) you need to manage your data for your plots, follow the example in "data_process_sidebar.py"
