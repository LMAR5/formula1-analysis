'''
Here will be stored all the plots required for Question 3 page

Create functions that have the following characteristics:
- Input: Iterable objects (Dataframes, arrays, dictionaries, etc.)
- Output: Plot object (can be Plotly, etc.)

Note: Refer to "plots/plots_q12.py" file to see an example
'''



def avg_pit_stop_duration(pit_stops: pd.DataFrame):
    # Group by race and calculate average pit stop duration
    avg_duration = (
        pit_stops.groupby('raceId')['duration']
        .mean()
        .reset_index()
        .rename(columns={'duration': 'avg_duration'})
    )

    # Create a bar chart
    bar_chart = px.bar(
        avg_duration,
        x='raceId',
        y='avg_duration',
        labels={'avg_duration': 'Average Pit Stop Duration (s)', 'raceId': 'Race ID'}
    )
    bar_chart.update_xaxes(type='category')
    return bar_chart



def driver_positions_after_pit_stops(merged_data: pd.DataFrame):
    # Focus on position and number of pit stops
    position_data = (
        merged_data.groupby(['driverId', 'stop'])['position']
        .mean()
        .reset_index()
        .rename(columns={'position': 'avg_position'})
    )

    # Create a scatter plot
    scatter_plot = px.scatter(
        position_data,
        x='stop',
        y='avg_position',
        color='driverId',
        labels={'stop': 'Number of Pit Stops', 'avg_position': 'Average Position'}
    )
    return scatter_plot


def lap_time_variation(merged_data: pd.DataFrame):
    # Calculate mean lap time before and after each stop
    lap_time_data = (
        merged_data.groupby(['stop', 'lap'])['milliseconds']
        .mean()
        .reset_index()
        .rename(columns={'milliseconds': 'avg_lap_time'})
    )

    # Create a line chart
    line_chart = px.line(
        lap_time_data,
        x='lap',
        y='avg_lap_time',
        color='stop',
        labels={'lap': 'Lap Number', 'avg_lap_time': 'Average Lap Time (ms)', 'stop': 'Pit Stop Number'}
    )
    return line_chart



def races_per_year(race_schedule: pd.DataFrame):
    # Count races per year
    races_per_year = (
        race_schedule.groupby('year')['raceId']
        .count()
        .reset_index()
        .rename(columns={'raceId': 'num_races'})
    )

    # Create a bar chart
    bar_chart = px.bar(
        races_per_year,
        x='year',
        y='num_races',
        labels={'num_races': 'Number of Races', 'year': 'Year'}
    )
    bar_chart.update_xaxes(type='category')
    return bar_chart