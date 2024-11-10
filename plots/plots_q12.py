'''
Here will be stored all the plots required for Question 1 and 2 pages

Create functions that have the following characteristics:
- Input: Iterable objects (Dataframes, arrays, dictionaries, etc.)
- Output: Plot object (can be Plotly, etc.)

'''

import plotly.express as px
import pandas as pd


def plot_constructor_performance(constructor_data: pd.DataFrame):
    '''
    Plots a stacked line chart for total points received by each constructor over the years.
        Args:
            - constructor_data (pd.DataFrame): DataFrame with 'name', 'year', and 'total_points' columns.
        Returns:
            - line chart object
    '''
    line_chart = px.line(
        constructor_data,
        x='year',
        y='total_points',
        color='name',  # Different color for each constructor
        labels={'total_points': 'Total Points', 'year': 'Year', 'name': 'Constructor'},
        title='Constructor Performance Over the Years'
    )
    
    # Update x-axis to show years as categories and improve visualization
    line_chart.update_xaxes(type='category')
    line_chart.update_layout(yaxis_title='Total Points', xaxis_title='Year')
    
    return line_chart

def plot_driver_performance(driver_data: pd.DataFrame):
    '''
    Plots a stacked line chart for total points received by each driver over the years.
        Args:
            - driver_data (pd.DataFrame): DataFrame with 'name', 'year', and 'total_points' columns.
        Returns:
            - line chart object
    '''
    line_chart = px.line(
        driver_data,
        x='year',
        y='total_points',
        color='name',  # Different color for each driver
        labels={'total_points': 'Total Points', 'year': 'Year', 'name': 'Driver'},
        title='Driver Performance Over the Years'
    )
    
    # Update x-axis to show years as categories and improve visualization
    line_chart.update_xaxes(type='category')
    line_chart.update_layout(yaxis_title='Total Points', xaxis_title='Year')
    
    return line_chart


