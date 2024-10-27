from pathlib import Path
import pandas as pd

# 1. Load data initial Dataframes directly from CSV files
app_dir = Path(__file__).parent.parent
teams_df = pd.read_csv(app_dir / "data/Team_Details.csv")
seasons_df = pd.read_csv(app_dir / "data/Season_Summaries.csv").sort_values(by='year')
tracks_df = pd.read_csv(app_dir / "data/Track_Information.csv")
drivers_df = pd.read_csv(app_dir / "data/Driver_Details.csv")


# 2. Create dictionaries, arrays, Dataframes, or whichever DS you need for your charts to export them

# Teams dictionary:  key -> Team ID (constructorId) and value -> Team's Name (name)
teams_dict = dict(zip(teams_df["constructorId"], teams_df["name"]))
# Seasons dictionary: key -> Season ID (index auto-generated) and value -> Season's year (int)
seasons_dict = dict()
for idx, team_year in enumerate(seasons_df["year"]):
    seasons_dict[idx] = team_year
# Tracks dictionary: key -> Track ID (circuitId) and value -> Track's Name (name)
tracks_dict = dict(zip(tracks_df["circuitId"], tracks_df["name"]))
# Drivers dictionary: key -> Driver ID (driverId) and value -> Driver's full name (forename + surname)
drivers_df["fullname"] = drivers_df["forename"] + " " + drivers_df["surname"]
drivers_dict = dict(zip(drivers_df["driverId"], drivers_df["fullname"]))