from pathlib import Path
import pandas as pd

# 1. Load data initial Dataframes directly from CSV files
app_dir = Path(__file__).parent.parent

## Load your CSV files here, follow the example in "data_process_sidebar.py"
teams_df = pd.read_csv(app_dir / "data/Team_Details.csv")
tracks_df = pd.read_csv(app_dir / "data/Track_Information.csv")
drivers_df = pd.read_csv(app_dir / "data/Driver_Details.csv")
race_schedule_df = pd.read_csv(app_dir / "data/Race_Schedule.csv")
race_results_df = pd.read_csv(app_dir / "data/Race_Results.csv")
qualifying_results_df = pd.read_csv(app_dir / "data/Qualifying_Results.csv")
sprint_results_df = pd.read_csv(app_dir / "data/Sprint_Race_Results.csv")
race_status_df = pd.read_csv(app_dir / "data/Race_Status.csv")

# 2. Create dictionaries, arrays, Dataframes, or whichever DS you need for your charts to export them

## Create the data structures (DS) you need to manage your data for your plots, follow the example in "data_process_sidebar.py"

# 1. From "race_schedule_df" get the columns "raceId", "year", and "circuitId"
_race_schedule_df = race_schedule_df[['raceId', 'year', 'circuitId']]
# 2. Join the "_race_schedule_df" and the "race_results_df" based on their common key "raceId"
_qualipos_racepts_df = _race_schedule_df.join(race_results_df[['raceId', 'driverId', 'constructorId','points','statusId']].set_index('raceId'), on='raceId')
# 3. Join the "_qualipos_racepts_df" and the "qualifying_results_df" based on the columns: raceId, driverId, constructorId
_qualipos_racepts_df = _qualipos_racepts_df.join(qualifying_results_df[['raceId', 'driverId', 'constructorId', 'position']].set_index(['raceId', 'driverId', 'constructorId']), on=['raceId', 'driverId', 'constructorId'])
# 4. Join the "_qualipos_racepts_df" and the "race_status_df" based on the columns: 
_qualipos_racepts_df = _qualipos_racepts_df.join(race_status_df[['statusId', 'status']].set_index('statusId'), on='statusId')
# 4. Join the "_qualipos_racepts_df" and the "sprint_results_df" based on the columns: raceId, driverId, constructorId
sprint_results_df.rename(columns={'points': 'Sprint_Pts'}, inplace=True)
_qualipos_racepts_df = _qualipos_racepts_df.join(sprint_results_df[['raceId', 'driverId', 'constructorId', 'Sprint_Pts']].set_index(['raceId', 'driverId', 'constructorId']), on=['raceId', 'driverId', 'constructorId'])
# 5. Add Drivers name, track Name
drivers_df["fullname"] = drivers_df["forename"] + " " + drivers_df["surname"]
_qualipos_racepts_df = _qualipos_racepts_df.join(drivers_df[['driverId', 'fullname']].set_index('driverId'), on='driverId')
# 6. Add teams name (for labels)
_qualipos_racepts_df = _qualipos_racepts_df.join(teams_df[['constructorId', 'name']].set_index('constructorId'), on='constructorId')
# 7. Add track names (for labels)
tracks_df.rename(columns={'location': 'Track'}, inplace=True)
_qualipos_racepts_df = _qualipos_racepts_df.join(tracks_df[['circuitId', 'Track']].set_index('circuitId'), on='circuitId')
# Fill missing values in columns "constructorId" and "driverId" with 0. No team has 0 (zero) as Id. 
_qualipos_racepts_df['constructorId'] = _qualipos_racepts_df["constructorId"].fillna(0)
_qualipos_racepts_df['driverId'] = _qualipos_racepts_df['driverId'].fillna(0)
_qualipos_racepts_df['points'] = _qualipos_racepts_df['points'].fillna(-1)
_qualipos_racepts_df['position'] = _qualipos_racepts_df['position'].fillna(-1)
_qualipos_racepts_df['Sprint_Pts'] = _qualipos_racepts_df['Sprint_Pts'].fillna(-1)
_qualipos_racepts_df['statusId'] = _qualipos_racepts_df['statusId'].fillna(-1)
_qualipos_racepts_df['status'] = _qualipos_racepts_df['status'].fillna("N/A")
# Convert the "constructorId", "driverId" columns from float to int.
_qualipos_racepts_df['constructorId'] = _qualipos_racepts_df['constructorId'].astype(int)
_qualipos_racepts_df['driverId'] = _qualipos_racepts_df['driverId'].astype(int)
_qualipos_racepts_df['points'] = _qualipos_racepts_df['points'].astype(int)
_qualipos_racepts_df['position'] = _qualipos_racepts_df['position'].astype(int)
_qualipos_racepts_df['Sprint_Pts'] = _qualipos_racepts_df['Sprint_Pts'].astype(int)
_qualipos_racepts_df['statusId'] = _qualipos_racepts_df['statusId'].astype(int)

# Rename columns that will appear in labels: "points" to "Race points", "position" to "Qualifying position", "fullname" to "Driver", "name" to "Team"
_qualipos_racepts_df.rename(columns={'points': 'Race_Pts', 'position': 'Qualifying_Pos', 'fullname': 'Driver', 'name': 'Team', 'status': 'Status'}, inplace=True)
_qualipos_racepts_df['idx'] = _qualipos_racepts_df.index
_qualipos_racepts_df['Total status'] = 1
