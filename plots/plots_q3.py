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
    # Ensure the 'duration' column is numeric
    pit_stops['duration'] = pd.to_numeric(pit_stops['duration'], errors='coerce')

    # Group by race and calculate average pit stop duration
    avg_duration = (
        pit_stops.groupby('name', as_index=False)['duration']
        .mean()
        .rename(columns={'duration': 'avg_duration'})
    )

    # Sort by average duration
    avg_duration = avg_duration.sort_values(by='avg_duration', ascending=False)

    # Create a bar chart
    bar_chart = px.bar(
        avg_duration,
        title='Comparing Pit Times',
        x='name',
        y='avg_duration',
        labels={'avg_duration': 'Average Pit Stop Duration (s)', 'name': 'Name'},
        color_discrete_sequence=['#ADD8E6']  # Neutral but visible color
    )

    # Dark theme :)
    bar_chart.update_layout(
        plot_bgcolor='rgb(30, 30, 30)',  # Dark background color for the plot
        paper_bgcolor='rgb(100, 100, 100)',  # Dark background color for the entire chart
        font=dict(color='white', size=12),  # White font for readability
        xaxis=dict(title=dict(font=dict(size=14)), tickangle=45),  # Adjust x-axis label angles
        yaxis=dict(title=dict(font=dict(size=14)))
    )

    return bar_chart


def scatter_wins_vs_pit_times(pit_stop_records: pd.DataFrame, highlight: pd.DataFrame):
    # Ensure 'duration' and 'wins' are numeric
    pit_stop_records['duration'] = pd.to_numeric(pit_stop_records['duration'], errors='coerce')
    pit_stop_records['wins'] = pd.to_numeric(pit_stop_records['wins'], errors='coerce')

    

    # Group by driver to calculate average pit stop times and total wins
    driver_stats = (
        pit_stop_records.groupby('driverId', as_index=False)
        .agg(
            avg_pit_time=('duration', 'mean'),
            wins=('wins', 'max')  # Assuming max wins per driver from rankings
        )
    )

    # Add a highlight column to identify highlighted drivers
    driver_stats['highlight'] = driver_stats['driverId'].apply(
        lambda x: 'Highlighted' if x in highlight['driverId'].values else 'Regular'
    )

    # Split data into highlighted and regular groups
    highlighted_data = driver_stats[driver_stats['highlight'] == 'Highlighted']
    regular_data = driver_stats[driver_stats['highlight'] == 'Regular']

    # Create scatter plot for regular data with its trendline
    scatter_regular = px.scatter(
        regular_data,
        x='wins',
        y='avg_pit_time',
        trendline='ols',
        labels={
            'wins': 'Number of Wins',
            'avg_pit_time': 'Average Pit Stop Duration (s)',
        },
        title='Wins vs. Average Pit Stop Times with Custom Trendlines',
        color_discrete_sequence=['#ADD8E6'],  # Light blue for regular points
        hover_data=['driverId']
    )

    scatter_regular.update_traces(
        line=dict(color='#a66623', width=1),  # Custom trendline color for highlighted data
        selector=dict(type='scatter', mode='lines')  # Apply only to the trendline
    )

    highlight_color ='#FFA07A'
    if len(set(highlight['name'])) > 100:
        highlight_color = '#ADD8E6'
        
    # Create scatter plot for highlighted data with its trendline
    scatter_highlighted = px.scatter(
        highlighted_data,
        x='wins',
        y='avg_pit_time',
        trendline='ols',
        labels={
            'wins': 'Number of Wins',
            'avg_pit_time': 'Average Pit Stop Duration (s)',
        },
        color_discrete_sequence=[highlight_color],  # Light red for highlighted points
        hover_data=['driverId']
    )

    scatter_highlighted.update_traces(
        line=dict(color='red', width=1),  # Custom trendline color for highlighted data
        selector=dict(type='scatter', mode='lines')  # Apply only to the trendline
    )

    # Combine traces from both plots
    for trace in scatter_highlighted.data:
        scatter_regular.add_trace(trace)

    # Customize layout
    scatter_regular.update_layout(
        plot_bgcolor='rgb(30, 30, 30)',  # Dark background for the plot
        paper_bgcolor='rgb(100, 100, 100)',  # Dark background for the chart
        font=dict(color='white', size=12),
        xaxis=dict(title=dict(font=dict(size=14)), tickangle=45),
        yaxis=dict(title=dict(font=dict(size=14))),
    )

    return scatter_regular