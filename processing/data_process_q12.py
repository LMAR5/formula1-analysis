from pathlib import Path
import pandas as pd

# 1. Load data initial Dataframes directly from CSV files
app_dir = Path(__file__).parent.parent

## Load your CSV files here, follow the example in "data_process_sidebar.py"
race_schedule = pd.read_csv(app_dir / "data/Race_Schedule.csv")

constructor_performance = pd.read_csv(app_dir / "data/Constructor_Performance.csv")
team_details = pd.read_csv(app_dir / "data/Team_Details.csv")

driver_ranking = pd.read_csv(app_dir / "data/Driver_Rankings.csv")
driver_details = pd.read_csv(app_dir / "data/Driver_Details.csv")

# 2. Create dictionaries, arrays, Dataframes, or whichever DS you need for your charts to export them

# get year from race_schedule and merge with constructor_performance on race ID
constructor_race_merged = pd.merge(constructor_performance, race_schedule[['raceId', 'year']], on='raceId')
# get name of constructor from team_details and merge with constructor_race_merged on constructor ID
constructor_race_team_merged = pd.merge(constructor_race_merged, team_details[['constructorId', 'name']], on='constructorId')
# group rows in merged df based on name and year, then sum points each team got over a given year
constructor_total_points_per_year = constructor_race_team_merged.groupby(['name', 'year'])['points'].sum().reset_index()
constructor_total_points_per_year.rename(columns={'points': 'total_points'}, inplace = True)

# assign total points of 0.0 for missing data/teams for some years
existing_years = constructor_total_points_per_year['year'].unique()
unique_constructors = constructor_total_points_per_year['name'].unique()
complete_index = pd.MultiIndex.from_product([unique_constructors, existing_years], names=['name', 'year'])
constructor_total_points_per_year = constructor_total_points_per_year.set_index(['name', 'year']).reindex(complete_index, fill_value=0.0).reset_index()
constructor_total_points_per_year.rename(columns={'points': 'total_points'}, inplace=True)
# Sort df by 'year' 
constructor_total_points_per_year = constructor_total_points_per_year.sort_values(by='year').reset_index(drop=True)

# get year from race_schedule and merge with driver_ranking on race ID 
driver_race_merged = pd.merge(driver_ranking, race_schedule[['raceId', 'year']], on='raceId')
# get name of driver from driver_details and merge with driver_race_merged on driver ID
driver_race_details_merged = pd.merge(driver_race_merged, driver_details[['driverId', 'forename', 'surname']], on='driverId')
# Create a new column 'name' that combines 'forename' and 'surname' for each driver
driver_race_details_merged['name'] = driver_race_details_merged['forename'] + ' ' + driver_race_details_merged['surname']
# Group by 'name' and 'year', and sum the points to get the total points each driver has earned per year
driver_total_points_per_year = driver_race_details_merged.groupby(['name', 'year'])['points'].sum().reset_index()
driver_total_points_per_year.rename(columns={'points': 'total_points'}, inplace=True)

# assign total points of 0.0 for missing data/drivers for some years
All_years = driver_total_points_per_year['year'].unique()
All_drivers = driver_total_points_per_year['name'].unique()
index = pd.MultiIndex.from_product([All_drivers, All_years], names=['name', 'year'])
driver_total_points_per_year = driver_total_points_per_year.set_index(['name', 'year']).reindex(index, fill_value=0.0).reset_index()
driver_total_points_per_year.rename(columns={'points': 'total_points'}, inplace=True)

# Sort df by 'year' 
driver_total_points_per_year = driver_total_points_per_year.sort_values(by='year').reset_index(drop=True)
## Create the data structures (DS) you need to manage your data for your plots, follow the example in "data_process_sidebar.py"
