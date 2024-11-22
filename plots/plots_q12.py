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
            - constructor_data (pd.DataFrame): DataFrame with 'name', 'year', and 'averagePoints' columns.
        Returns:
            - line chart object
    '''
    line_chart = px.line(
        constructor_data,
        x='year',
        y='averagePoints',
        color='name',  # Different color for each constructor
        labels={'averagePoints': 'Average Points', 'year': 'Year', 'name': 'Constructor'},
        title='Constructor Performance Over the Years'
    )
    
    # Update x-axis to show years as categories and improve visualization
    line_chart.update_xaxes(type='category')
    line_chart.update_layout(yaxis_title='Average Points', xaxis_title='Year')
    
    return line_chart

def plot_driver_performance(driver_data: pd.DataFrame):
    '''
    Plots a stacked line chart for total points received by each driver over the years.
        Args:
            - driver_data (pd.DataFrame): DataFrame with 'name', 'year', and 'averagePoints' columns.
        Returns:
            - line chart object
    '''
    line_chart = px.line(
        driver_data,
        x='year',
        y='averagePoints',
        color='name',  # Different color for each driver
        labels={'averagePoints': 'Average Points', 'year': 'Year', 'name': 'Driver'},
        title='Driver Performance Over the Years'
    )
    
    # Update x-axis to show years as categories and improve visualization
    line_chart.update_xaxes(type='category')
    line_chart.update_layout(yaxis_title='Average Points', xaxis_title='Year')
    
    return line_chart

def plot_top_10_drivers(driver_data: pd.DataFrame):
    '''
    Plots a bar chart for the top 10 drivers with the highest average points.
        Args:
            - driver_data (pd.DataFrame): DataFrame with 'name' and 'averagePoints' columns.
        Returns:
            - bar chart object
    '''
    bar_chart = px.bar(
        driver_data,
        x='name',
        y='averagePoints',
        labels={'averagePoints': 'Average Points', 'name': 'Driver'},
        title='Top 10 Drivers by Average Points'
    )
    
    # Update layout to improve visualization
    bar_chart.update_layout(xaxis_title='Driver', yaxis_title='Average Points')
    
    return bar_chart


def plot_top_10_teams(constructor_data: pd.DataFrame):
    '''
    Plots a bar chart for the top 10 drivers with the highest average points.
        Args:
            - constructor_data (pd.DataFrame): DataFrame with 'name' and 'averagePoints' columns.
        Returns:
            - bar chart object
    '''
    bar_chart = px.bar(
        constructor_data,
        x='name',
        y='averagePoints',
        labels={'averagePoints': 'Average Points', 'name': 'Team'},
        title='Top 10 Teams by Average Points'
    )
    
    # Update layout to improve visualization
    bar_chart.update_layout(xaxis_title='Teams', yaxis_title='Average Points')
    
    return bar_chart

