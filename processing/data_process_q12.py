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

# Setup constructor data frames

# get year from race_schedule and merge with constructor_performance on race ID
constructor_race_merged = pd.merge(constructor_performance, race_schedule[['raceId', 'year']], on='raceId')
# get name of constructor from team_details and merge with constructor_race_merged on constructor ID
constructor_race_team_merged = pd.merge(constructor_race_merged, team_details[['constructorId', 'name']], on='constructorId')
# group rows in merged df based on name and year, then sum points each team got over a given year
constructor_total_points_per_year = constructor_race_team_merged.groupby(['constructorId','name', 'year'])['points'].sum().reset_index()
constructor_total_points_per_year.rename(columns={'points': 'total_points'}, inplace = True)

# Sort df by 'year' 
constructor_total_points_per_year = constructor_total_points_per_year.sort_values(by='year').reset_index(drop=True)

# Group by constructorId and year, and count the number of rows
constructor_raceCount = constructor_race_merged.groupby(['constructorId', 'year'])['raceId'].count().reset_index()
constructor_raceCount.columns = ['constructorId', 'year', 'raceCount']

constructor_raceCount = constructor_raceCount.sort_values(by='year').reset_index(drop=True)
# Merge constructor_total_points_per_year with constructor_raceCount
constructor_average_points_per_year = pd.merge(constructor_total_points_per_year, constructor_raceCount, on=['constructorId', 'year'])

# Calculate average points per year for each constructor
constructor_average_points_per_year['averagePoints'] = constructor_average_points_per_year['total_points'] / constructor_average_points_per_year['raceCount']


# DF will be used to plot top 10 constructors of all time based on all points accumulated by each driver

# Group by constructorId and name, and sum the average points
constructor_total_average_points = constructor_average_points_per_year.groupby(['constructorId', 'name'])['averagePoints'].sum().reset_index()

# Sort the DataFrame in descending order by average points
constructor_total_average_points = constructor_total_average_points.sort_values(by='averagePoints', ascending=False).reset_index(drop=True)

# Select only the top 10 drivers
constructor_top_10_average_points = constructor_total_average_points.head(10)

# Setup driver details

# get year from race_schedule and merge with driver_ranking on race ID 
driver_race_merged = pd.merge(driver_ranking, race_schedule[['raceId', 'year']], on='raceId')
# get name of driver from driver_details and merge with driver_race_merged on driver ID
driver_race_details_merged = pd.merge(driver_race_merged, driver_details[['driverId', 'forename', 'surname']], on='driverId')
# Create a new column 'name' that combines 'forename' and 'surname' for each driver
driver_race_details_merged['name'] = driver_race_details_merged['forename'] + ' ' + driver_race_details_merged['surname']
# Group by 'name' and 'year', and sum the points to get the total points each driver has earned per year
driver_total_points_per_year = driver_race_details_merged.groupby(['driverId','name', 'year'])['points'].sum().reset_index()
driver_total_points_per_year.rename(columns={'points': 'total_points'}, inplace=True)

# Sort df by 'year' 
driver_total_points_per_year = driver_total_points_per_year.sort_values(by='year').reset_index(drop=True)

driver_raceCount = driver_race_merged.groupby(['driverId', 'year'])['raceId'].count().reset_index()
driver_raceCount.columns = ['driverId', 'year', 'raceCount']

driver_raceCount = driver_raceCount.sort_values(by='year').reset_index(drop=True)

# Merge driver_total_points_per_year with driver_raceCount
driver_average_points_per_year = pd.merge(driver_total_points_per_year, driver_raceCount, on=['driverId', 'year'])

# Calculate average points per year for each driver
driver_average_points_per_year['averagePoints'] = driver_average_points_per_year['total_points'] / driver_average_points_per_year['raceCount']


# DF will be used to plot top 10 drivers of all time based on all points accumulated by each driver

# Group by driverId and name, and sum the average points
driver_total_average_points = driver_average_points_per_year.groupby(['driverId', 'name'])['averagePoints'].sum().reset_index()

# Sort the DataFrame in descending order by average points
driver_total_average_points = driver_total_average_points.sort_values(by='averagePoints', ascending=False).reset_index(drop=True)

# Select only the top 10 drivers
driver_top_10_average_points = driver_total_average_points.head(10)