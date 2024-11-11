import faicons as fa
import plotly.express as px

# Load data and compute static values
from processing.data_process_sidebar import teams_dict, seasons_dict, tracks_dict, drivers_dict, _select_filters_df
from processing.data_process_q12 import app_dir, race_schedule_df
from processing.data_process_q3 import app_dir
from processing.data_process_q45 import app_dir, _qualipos_racepts_df
from shinywidgets import render_plotly

from shiny import reactive, render
from shiny.express import input, ui

# Load plot functions
from plots.plots_q12 import num_driver_per_season
from plots.plots_q45 import qualipos_racepts_scatterplot, sprintpts_racepts_scatterplot, status_by_driver_piechart

# Page title
ui.page_opts(title="Formula 1 Analysis")

# The sidebar is shared across all question pages
with ui.sidebar():
    ui.input_selectize(
        "select_season", # ID
        "Select a season:", # Label
        choices=seasons_dict, # Options
        remove_button=True, # Reset the select input component
        multiple=True,
        options={"plugins": ["clear_button"]}
    )
    ui.input_selectize(
        "select_track",
        "Select a track:",
        choices=tracks_dict,
        remove_button=True,
        multiple=True,
        options={"plugins": ["clear_button"]}
    )
    ui.input_selectize(
        "select_team",
        "Select a team:",
        choices=teams_dict,
        remove_button=True,
        multiple=True,
        options={"plugins": ["clear_button"]}
    )
    ui.input_selectize(
        "select_driver",
        "Select a driver:",
        choices=drivers_dict,
        remove_button=True,
        multiple=True,
        options={"plugins": ["clear_button"]}
    )
    ui.input_action_button("reset", "Reset filters")

    @render.text
    def season():
        return f"Selected [Season ID]: {input.select_season()}"
    @render.text
    def track():
        return f"Selected [Track ID]: {input.select_track()}"
    @render.text
    def team():
        return f"Selected [Team ID]: {input.select_team()}"
    @render.text
    def driver():
        return f"Selected [Driver ID]: {input.select_driver()}"

# Content for each Question page
with ui.nav_panel("Question 1"):
    ui.h4("Question 1")
    with ui.layout_columns():
        with ui.card(full_screen=True):
            ui.card_header("Number of races across seasons")
            @render_plotly
            def drivers_season():
                return num_driver_per_season(drivers_per_sel_season())


with ui.nav_panel("Question 2"):
    ui.h4("Question 2 content")

with ui.nav_panel("Question 3"):
    ui.h4("Question 3 content")

with ui.nav_panel("Question 4"):
    ui.h4("How can qualifying sessions and sprints impact drivers performance?")
    with ui.layout_columns(col_widths={"sm": (6,6,5,7)}):
        with ui.card(full_screen=True):
            ui.card_header("Qualifying position vs Race points")
            @render_plotly
            def quali_sprints_plot_q4():
                return qualipos_racepts_scatterplot(qualipos_racepts_data_q4())

        with ui.card(full_screen=True):
            ui.card_header("Sprint points vs Race points")
            @render_plotly
            def sprint_race_pts_plot_q4():
                return sprintpts_racepts_scatterplot(sprintpts_racepts_data_q4())

        with ui.card(full_screen=True):
            ui.card_header("Status of races by Driver")
            @render_plotly
            def status_races_q4():
                return status_by_driver_piechart(race_status_data_q4())

        with ui.card(full_screen=True):
            ui.card_header("Summary of races per driver")
            @render.data_frame
            def races_summary_q4():
                return render.DataGrid(summary_data_q4(), styles=[{"style": {"font-size": "0.8em"}}])
        

with ui.nav_panel("Question 5"):
    ui.h4("Which team has provided the most talented drivers throughout the years?")
    with ui.layout_columns(col_widths={"sm": (6,6,5,7)}):
        with ui.card(full_screen=True):
            ui.card_header("Number of drivers per constructor team")
            @render.plot
            def drivers_per_constructor_q5():
                pass
        with ui.card(full_screen=True):
            ui.card_header("Total of points by driver")
            @render.plot
            def points_per_driver_q5():
                pass
        with ui.card(full_screen=True):
            ui.card_header("Most completed races by driver")
            @render.plot
            def completed_per_driver_q5():
                pass
        with ui.card(full_screen=True):
            ui.card_header("Summary of races per driver")
            @render.plot
            def races_summary_q5():
                pass



# ------------------------------------------------------------------
# Reactive calculations and effects
# ------------------------------------------------------------------

# Reactive calculation and effects for sidebar
# Author: N/A
# --------------------------------------------------------
def update_dict(old_dic: dict, lst_values, type: str="") -> dict:
    tmp_dict = dict()
    for key, value in old_dic.items():
        if type == "season":
            if value in lst_values:
                tmp_dict[key] = value
        else:
            if key in lst_values:
                tmp_dict[key] = value
    return tmp_dict

def filter_df_by_selection(all_data, selected_tuple: tuple, type: str):
    if len(selected_tuple) > 0:
        if selected_tuple[0] is not None:
            selected_entity_lst: list[int] = []
            for item in selected_tuple:
                if type == "season":
                    selected_entity_lst.append(seasons_dict[int(item)])
                else:
                    selected_entity_lst.append(int(item))
            if type == "season":
                all_data = all_data[all_data['year'].isin(selected_entity_lst)]
            elif type == "track":
                all_data = all_data[all_data['circuitId'].isin(selected_entity_lst)]
            elif type == "team":
                all_data = all_data[all_data['constructorId'].isin(selected_entity_lst)]
            elif type == "driver":
                all_data = all_data[all_data['driverId'].isin(selected_entity_lst)]
    return all_data

@reactive.effect
def filter_sidebar_tracks():
    selected_season_tuple: tuple = input.select_season()
    selected_team_tuple: tuple = input.select_team()
    selected_driver_tuple: tuple = input.select_driver()
    selected_track_tuple: tuple = input.select_track()
    tmp_lst = _select_filters_df.copy()
    tmp_lst = filter_df_by_selection(tmp_lst, selected_season_tuple, "season")
    tmp_lst = filter_df_by_selection(tmp_lst, selected_team_tuple, "team")
    tmp_lst = filter_df_by_selection(tmp_lst, selected_track_tuple, "track")
    tmp_lst = filter_df_by_selection(tmp_lst, selected_driver_tuple, "driver")
    tmp_seasons_lst = tmp_lst[['year']]
    new_seasons_dict = update_dict(seasons_dict, tmp_seasons_lst.values, "season")
    selected_seasons_lst: list[str] = []
    for item in selected_season_tuple:
        selected_seasons_lst.append(item)
    ui.update_selectize("select_season", choices=new_seasons_dict, selected=selected_seasons_lst)
    tmp_tracks_lst = tmp_lst[['circuitId']]
    new_tracks_dict = update_dict(tracks_dict, tmp_tracks_lst.values)
    selected_tracks_lst: list[int] = []
    for item in selected_track_tuple:
        selected_tracks_lst.append(int(item))
    ui.update_selectize("select_track", choices=new_tracks_dict, selected=selected_tracks_lst)
    tmp_teams_lst = tmp_lst[['constructorId']]
    new_teams_dict = update_dict(teams_dict, tmp_teams_lst.values)
    selected_teams_lst: list[int] = []
    for item in selected_team_tuple:
        selected_teams_lst.append(int(item))
    ui.update_selectize("select_team", choices=new_teams_dict, selected=selected_teams_lst)    
    tmp_drivers_lst = tmp_lst[['driverId']]
    new_drivers_dict = update_dict(drivers_dict, tmp_drivers_lst.values)
    selected_drivers_lst: list[int] = []
    for item in selected_driver_tuple:
        selected_drivers_lst.append(int(item))
    ui.update_selectize("select_driver", choices=new_drivers_dict, selected=selected_drivers_lst)

@reactive.effect
@reactive.event(input.reset)
def _():
    ui.update_selectize("select_season", choices=seasons_dict)
    ui.update_selectize("select_team", choices=teams_dict)
    ui.update_selectize("select_driver", choices=drivers_dict)
    ui.update_selectize("select_track", choices=tracks_dict)

    

# Reactive calculation and effects for Questions 1 and 2
# Author: Siham Argaw
# --------------------------------------------------------

# Reactive function that triggers depending if an input variable changes (season - select box)
# Link: https://shiny.posit.co/py/api/express/reactive.calc.html
@reactive.calc
def drivers_per_sel_season():
    # Get the selected season by the end user
    selected_season_tuple: tuple = input.select_season()
    # Filter the race list to only 2 columns: raceId and year
    lst_races = race_schedule_df[['raceId', 'year']]
    # If a season was chosen in the select box
    if len(selected_season_tuple) > 0:
        if selected_season_tuple[0] is not None:
            # From the select box, get the selected years in a list
            selected_season_lst: list[int] = []
            for item in selected_season_tuple:
                selected_season_lst.append(seasons_dict[int(item)])
            # Filter the drivers data by the selected seasons
            lst_races = lst_races[lst_races['year'].isin(selected_season_lst)]
    # Group the race list by the 'year' and count the number of 'raceId' per 'year'
    lst_races = lst_races.groupby('year').count().reset_index()
    return lst_races

## Write your functions for Q1 and Q2 here


# Reactive calculation and effects for Question 3
# Author: Matthew Bush
# --------------------------------------------------------

## Write your functions for Q3 here


# Reactive calculation and effects for Questions 4 and 5
# Author: Luis Aguilar
# --------------------------------------------------------

## Write your functions for Q4 and Q5 here
@reactive.calc
def qualipos_racepts_data_q4():
    selected_season_tuple: tuple = input.select_season()
    selected_track_tuple: tuple = input.select_track()
    selected_team_tuple: tuple = input.select_team()
    selected_driver_tuple: tuple = input.select_driver()
    lst_data = _qualipos_racepts_df[['idx','raceId','year','circuitId','driverId','constructorId', 'Race_Pts', 'Qualifying_Pos']]
    lst_data = filter_df_by_selection(lst_data, selected_season_tuple, "season")
    lst_data = filter_df_by_selection(lst_data, selected_track_tuple, "track")
    lst_data = filter_df_by_selection(lst_data, selected_team_tuple, "team")
    lst_data = filter_df_by_selection(lst_data, selected_driver_tuple, "driver")
    return lst_data

@reactive.calc
def sprintpts_racepts_data_q4():
    selected_season_tuple: tuple = input.select_season()
    selected_track_tuple: tuple = input.select_track()
    selected_team_tuple: tuple = input.select_team()
    selected_driver_tuple: tuple = input.select_driver()
    lst_data = _qualipos_racepts_df[['idx','raceId','year','circuitId','driverId','constructorId', 'Race_Pts', 'Sprint_Pts']]
    lst_data = filter_df_by_selection(lst_data, selected_season_tuple, "season")
    lst_data = filter_df_by_selection(lst_data, selected_track_tuple, "track")
    lst_data = filter_df_by_selection(lst_data, selected_team_tuple, "team")
    lst_data = filter_df_by_selection(lst_data, selected_driver_tuple, "driver")
    return lst_data

@reactive.calc
def race_status_data_q4():
    selected_season_tuple: tuple = input.select_season()
    selected_track_tuple: tuple = input.select_track()
    selected_team_tuple: tuple = input.select_team()
    selected_driver_tuple: tuple = input.select_driver()
    lst_data = _qualipos_racepts_df[['idx','raceId','year','circuitId','driverId','constructorId', 'statusId', 'Status', 'Total status']]
    lst_data = filter_df_by_selection(lst_data, selected_season_tuple, "season")
    lst_data = filter_df_by_selection(lst_data, selected_track_tuple, "track")
    lst_data = filter_df_by_selection(lst_data, selected_team_tuple, "team")
    lst_data = filter_df_by_selection(lst_data, selected_driver_tuple, "driver")
    lst_data = lst_data[['idx', 'statusId', 'Status', 'Total status']]
    return lst_data

@reactive.calc
def summary_data_q4():
    selected_season_tuple: tuple = input.select_season()
    selected_track_tuple: tuple = input.select_track()
    selected_team_tuple: tuple = input.select_team()
    selected_driver_tuple: tuple = input.select_driver()
    summary_data = _qualipos_racepts_df.copy()
    summary_data = filter_df_by_selection(summary_data, selected_season_tuple, "season")
    summary_data = filter_df_by_selection(summary_data, selected_track_tuple, "track")
    summary_data = filter_df_by_selection(summary_data, selected_team_tuple, "team")
    summary_data = filter_df_by_selection(summary_data, selected_driver_tuple, "driver")
    summary_data['Sprint_Pts'] = summary_data['Sprint_Pts'].astype(str)
    summary_data['Sprint_Pts'] = summary_data['Sprint_Pts'].replace('-1', 'N/A')
    summary_data = summary_data[['year', 'Team', 'Driver', 'Sprint_Pts', 'Qualifying_Pos', 'Race_Pts', 'Status']]
    return summary_data