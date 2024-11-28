import faicons as fa
import plotly.express as px

# Load data and compute static values
from processing.data_process_sidebar import teams_dict, seasons_dict, tracks_dict, drivers_dict, _select_filters_df
from processing.data_process_q12 import app_dir, race_schedule_df
from processing.data_process_q3 import app_dir
from processing.data_process_q45 import app_dir
from shinywidgets import render_plotly

from shiny import reactive, render
from shiny.express import input, ui

# Load plot functions
from plots.plots_q12 import num_driver_per_season

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
    ui.h4("Question 4 content")

with ui.nav_panel("Question 5"):
    ui.h4("Question 5 content")



# ------------------------------------------------------------------
# Reactive calculations and effects
# ------------------------------------------------------------------

# Reactive calculation and effects for sidebar
# Author: N/A
# --------------------------------------------------------
def update_dict(old_dic: dict, lst_values) -> dict:
    tmp_dict = dict()
    for key, value in old_dic.items():
        if key in lst_values:
            tmp_dict[key] = value
    return tmp_dict

# Function that filters all select boxes based on the selected season
@reactive.effect
def filter_sidebar_seasons() -> None:
    selected_season_tuple: tuple = input.select_season()
    # If a season was chosen in the select box
    if len(selected_season_tuple) > 0:
        if selected_season_tuple[0] is not None:
            # Get season years and filter dataframe by selected seasons
            selected_seasons_lst: list[int] = []
            for item in selected_season_tuple:
                selected_seasons_lst.append(seasons_dict[int(item)])
            tmp_lst = _select_filters_df[_select_filters_df['year'].isin(selected_seasons_lst)]
            # Filter the teams select box options
            tmp_teams_lst = tmp_lst[['constructorId']]
            new_teams_dict = update_dict(teams_dict, tmp_teams_lst.values)
            ui.update_selectize("select_team", choices=new_teams_dict)
            # Filter the tracks/circuits select box options
            tmp_tracks_lst = tmp_lst[['circuitId']]
            new_tracks_dict = update_dict(tracks_dict, tmp_tracks_lst.values)
            ui.update_selectize("select_track", choices=new_tracks_dict)
            # Filter the drivers select box options
            tmp_drivers_lst = tmp_lst[['driverId']]
            new_drivers_dict = update_dict(drivers_dict, tmp_drivers_lst.values)
            ui.update_selectize("select_driver", choices=new_drivers_dict)
        else:
            # If no year is selected, show all available values
            ui.update_selectize("select_team", choices=teams_dict)
            ui.update_selectize("select_track", choices=tracks_dict)
            ui.update_selectize("select_driver", choices=drivers_dict)

# Function that filters the driver's select box based on the selected season, team, and track
@reactive.effect
def filter_sidebar_drivers() -> None:
    # Get the user's selected values in the select boxes (season, team, track)
    selected_season_tuple: tuple = input.select_season()
    selected_team_tuple: tuple = input.select_team()
    selected_track_tuple: tuple = input.select_track()
    # If a season was chosen in the select box
    if len(selected_season_tuple) > 0:
        if selected_season_tuple[0] is not None:
            # Get seasons years and filter dataframe by selected seasons
            selected_seasons_lst: list[int] = []
            for item in selected_season_tuple:
                selected_seasons_lst.append(seasons_dict[int(item)])
            tmp_lst = _select_filters_df[_select_filters_df['year'].isin(selected_seasons_lst)]
            # If teams were selected, filter the list of drivers by the selected teams
            if len(selected_team_tuple) > 0:
                if selected_team_tuple[0] is not None:
                    selected_teams_lst: list[int] = []
                    for item in selected_team_tuple:
                        selected_teams_lst.append(int(item))
                    tmp_lst = tmp_lst[tmp_lst['constructorId'].isin(selected_teams_lst)]
            # If tracks were selected, filter the list of drivers by the selected tracks
            if len(selected_track_tuple) > 0:
                if selected_track_tuple[0] is not None:
                    selected_tracks_lst: list[int] = []
                    for item in selected_track_tuple:
                        selected_tracks_lst.append(int(item))
                    tmp_lst = tmp_lst[tmp_lst['circuitId'].isin(selected_tracks_lst)]
            # Filter the drivers select box options
            tmp_drivers_lst = tmp_lst[['driverId']]
            new_drivers_dict = update_dict(drivers_dict, tmp_drivers_lst.values)
            ui.update_selectize("select_driver", choices=new_drivers_dict)
        else:
            # If no year is selected, show all available drivers
            ui.update_selectize("select_driver", choices=drivers_dict)


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
# How have pit stop Umings and strategies affected race outcomes?






# Reactive calculation and effects for Questions 4 and 5
# Author: Luis Aguilar
# --------------------------------------------------------

## Write your functions for Q4 and Q5 here
