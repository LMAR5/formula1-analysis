'''
Here will be stored all the plots required for Question 3 page

Create functions that have the following characteristics:
- Input: Iterable objects (Dataframes, arrays, dictionaries, etc.)
- Output: Plot object (can be Plotly, etc.)

Note: Refer to "plots/plots_q12.py" file to see an example
'''
import plotly.express as px
import pandas as pd


def avg_pit_stop_duration(pit_stops: pd.DataFrame):
    # Group by race and calculate average pit stop duration

    '''
    avg_duration = (
        pit_stops.groupby('raceId')['duration']
        .mean()
        .reset_index()
        .rename(columns={'duration': 'avg_duration'})
    )'''

    # Create a bar chart
    bar_chart = px.bar(
        pit_stops,
        y='raceId',
        x='duration',
        labels={'avg_duration': 'Average Pit Stop Duration (s)', 'raceId': 'Race ID'}
    )
    bar_chart.update_xaxes(type='category')
    return bar_chart
