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
        selected=74, # Pre selected season: 2024
        remove_button=True # Reset the select input component
    )
    ui.input_selectize(
        "select_track",
        "Select a track:",
        choices=tracks_dict,
        remove_button=True
    )
    ui.input_selectize(
        "select_team",
        "Select a team:",
        choices=teams_dict,
        remove_button=True
    )
    ui.input_selectize(
        "select_driver",
        "Select a driver:",
        choices=drivers_dict,
        remove_button=True
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

@reactive.effect
def filter_sidebar_seasons():
    selected_season_id = input.select_season()
    if selected_season_id != "":
        # Get season year and filter dataframe by selected season
        selected_season_id = int(selected_season_id)
        selected_season_year = seasons_dict[selected_season_id]
        tmp_lst = _select_filters_df[_select_filters_df['year'] == selected_season_year]
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


# Reactive calculation and effects for Questions 1 and 2
# Author: Siham Argaw
# --------------------------------------------------------

# Reactive function that triggers depending if an input variable changes (season - select box)
# Link: https://shiny.posit.co/py/api/express/reactive.calc.html
@reactive.calc
def drivers_per_sel_season():
    # Get the selected season by the end user
    selected_season_id = input.select_season()
    # Filter the race list to only 2 columns: raceId and year
    lst_races = race_schedule_df[['raceId', 'year']]
    if selected_season_id != "":
        selected_season_id = int(selected_season_id)
        # From the select box, get the year
        selected_season = seasons_dict[selected_season_id]
        # Filter the drivers data by the selected season
        lst_races = lst_races[lst_races['year'] == selected_season]
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
