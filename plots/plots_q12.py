'''
Here will be stored all the plots required for Question 1 and 2 pages

Create functions that have the following characteristics:
- Input: Iterable objects (Dataframes, arrays, dictionaries, etc.)
- Output: Plot object (can be Plotly, etc.)

'''

import plotly.express as px
import pandas as pd

def num_driver_per_season(races: pd.DataFrame):
    bar_chart = px.bar(
        races,
        x = 'year',
        y = 'raceId',
        labels={'raceId': 'Number of races'}
    )
    bar_chart.update_xaxes(type='category')
    return bar_chart
