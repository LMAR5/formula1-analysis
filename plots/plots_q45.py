'''
Here will be stored all the plots required for Question 4 and 5 pages

Create functions that have the following characteristics:
- Input: Iterable objects (Dataframes, arrays, dictionaries, etc.)
- Output: Plot object (can be Plotly, etc.)

Note: Refer to "plots/plots_q12.py" file to see an example
'''
import plotly.express as px
import pandas as pd

def qualipos_racepts_scatterplot(data: pd.DataFrame):
    # The "-1" values are inconsistent data from the dataset that will not be in the scope of this chart
    data = data[data['Qualifying_Pos'] > -1]
    data = data[data['Race_Pts'] > -1]
    if len(data.index) == 0:
        scatter_plot = px.scatter(
            {'Qualifying_Pos': [], 'Race_Pts': []}, 
            x="Race_Pts", 
            y="Qualifying_Pos",
            labels={'Qualifying_Pos':'Qualifying position', 'Race_Pts': 'Race points'}
        )
    else:
        data['count'] = data.groupby(['Race_Pts', 'Qualifying_Pos'])['Race_Pts'].transform('count')
        scatter_plot = px.scatter(
            data, 
            x="Race_Pts", 
            y="Qualifying_Pos", 
            labels={'Qualifying_Pos':'Qualifying position', 'Race_Pts': 'Race points'},
            size='count',
            hover_data=['count']
        )
        scatter_plot.update_yaxes(autorange="reversed")
        scatter_plot.update_traces(text=data['count'], textposition='top center')
    return scatter_plot

def sprintpts_racepts_scatterplot(data: pd.DataFrame):
    # The "-1" values are inconsistent data from the dataset that will not be in the scope of this chart
    data = data[data['Sprint_Pts'] > -1]
    if len(data.index) == 0:
        scatter_plot = px.scatter(
            {'Sprint_Pts': [], 'Race_Pts': []}, 
            x="Race_Pts", 
            y="Sprint_Pts",
            labels={'Sprint_Pts':'Sprint points', 'Race_Pts': 'Race points'}
            )
    else:
        data['count'] = data.groupby(['Sprint_Pts', 'Race_Pts'])['Sprint_Pts'].transform('count')
        scatter_plot = px.scatter(
            data, 
            x="Race_Pts", 
            y="Sprint_Pts", 
            labels={'Sprint_Pts':'Sprint points', 'Race_Pts': 'Race points'},
            size="count",
            hover_data=['count', 'year']
        )
        scatter_plot.update_traces(text=data['count'], textposition='top center')
    return scatter_plot

def status_by_driver_piechart(data: pd.DataFrame):
    pie_chart = px.pie(
        data,
        names='Status',
        values='Total status'
    )
    return pie_chart