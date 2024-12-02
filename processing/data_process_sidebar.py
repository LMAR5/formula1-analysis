from pathlib import Path
import pandas as pd

# 1. Load data initial Dataframes directly from CSV files
app_dir = Path(__file__).parent.parent
teams_df = pd.read_csv(app_dir / "data/Team_Details.csv")
seasons_df = pd.read_csv(app_dir / "data/Season_Summaries.csv").sort_values(by='year')
tracks_df = pd.read_csv(app_dir / "data/Track_Information.csv")
drivers_df = pd.read_csv(app_dir / "data/Driver_Details.csv")
# To build internal dataframe that will be used to filter all select boxes
race_schedule_df = pd.read_csv(app_dir / "data/Race_Schedule.csv")
race_results_df = pd.read_csv(app_dir / "data/Race_Results.csv")



# 2. Create dictionaries, arrays, Dataframes, or whichever DS you need for your charts to export them

# Teams dictionary:  key -> Team ID (constructorId) and value -> Team's Name (name)
teams_dict = dict(zip(teams_df["constructorId"], teams_df["name"]))
# Seasons dictionary: key -> Season ID (index auto-generated) and value -> Season's year (int)
seasons_dict = dict()
for idx, team_year in enumerate(seasons_df["year"]):
    seasons_dict[idx] = team_year
# Tracks dictionary: key -> Track ID (circuitId) and value -> Track's Name (location)
tracks_dict = dict(zip(tracks_df["circuitId"], tracks_df["location"]))
# Drivers dictionary: key -> Driver ID (driverId) and value -> Driver's full name (forename + surname)
drivers_df["fullname"] = drivers_df["forename"] + " " + drivers_df["surname"]
drivers_dict = dict(zip(drivers_df["driverId"], drivers_df["fullname"]))


# Build internal dataframe to filter all select boxes
# ----------------------------------------------------------------
# Table columns: raceId, year, teamId, trackId, driverId

# 1. From "race_schedule_df" get the columns "raceId", "year", and "circuitId"
_select_filters_df = race_schedule_df[['raceId', 'year', 'circuitId']]

# 2. Join the "race_schedule_df" and the "race_results_df" based on their common key "raceId"
_select_filters_df = _select_filters_df.join(race_results_df[['raceId', 'driverId', 'constructorId']].set_index('raceId'), on='raceId')

# Fill missing values in columns "constructorId" and "driverId" with 0.
# - Problem: Some results of some races were not mapped in Dataset. For example, some races of 2024 have not been updated yet.
# - Solution: Since no team or driver has an Id=0, we'll fill the N/A values with 0 (zero) to avoid mismatching issues.
_select_filters_df['constructorId'] = _select_filters_df["constructorId"].fillna(0)
_select_filters_df['driverId'] = _select_filters_df['driverId'].fillna(0)
# Convert the "constructorId", "driverId" columns from float to int.
_select_filters_df['constructorId'] = _select_filters_df['constructorId'].astype(int)
_select_filters_df['driverId'] = _select_filters_df['driverId'].astype(int)

'''
Example result of "_select_filters_df" dataframe

Goal: Use this internal dataframe to filter the select boxes that the end user interacts with.
Use case: If user selects the "2021" season, it will filter the rest of select boxes (teams, tracks, and drivers) based on the selected season year.

Year: 2021
Races: Monza (1), SPA (2)
Circuits: Autodromo Nazionale di Monza (6), Circuit de Spa-Francorchamps (13)
Constructors: Red Bull (9), Ferrari (6)
driverId: Max Verstappen (830), Charles Leclerc (277)

raceId | year | circuitId | constructorId | driverId |
------------------------------------------------------
   1   | 2021 |     6     |       9       |    830   |
   1   | 2021 |     6     |       6       |    277   |
   2   | 2021 |     13    |       9       |    830   |
   2   | 2021 |     13    |       6       |    277   |
'''
   
# EOF
