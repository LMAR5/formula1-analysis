import faicons as fa
import plotly.express as px

# Load data and compute static values
from processing.data_process_sidebar import teams_dict, seasons_dict, tracks_dict, drivers_dict, _select_filters_df
from processing.data_process_q12 import app_dir, constructor_average_points_per_year, driver_average_points_per_year, driver_top_10_average_points, constructor_top_10_average_points
from processing.data_process_q3 import app_dir, q3_dataframes, basic_pits
from processing.data_process_q45 import app_dir, _qualipos_racepts_df
from shinywidgets import render_plotly

from shiny import reactive, render
from shiny.express import input, ui

# Load plot functions
from plots.plots_q12 import plot_constructor_performance, plot_driver_performance, plot_top_10_drivers, plot_top_10_teams
from plots.plots_q3 import avg_pit_stop_duration, scatter_wins_vs_pit_times, histogram_pit_stop_laps, bubble_chart_wins_vs_pit_duration
from plots.plots_q45 import qualipos_racepts_scatterplot, sprintpts_racepts_scatterplot, status_by_driver_piechart, drivers_per_team_barchart_q5, points_per_driver_barchart_q5, races_per_driver_barchart_q5

# Page title
ui.page_opts(title="Formula 1 Analysis")
ui.head_content(ui.tags.link(rel="icon", type="image/x-icon", href="favicon.ico"))

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

    # @render.text
    # def season():
    #     return f"Selected [Season ID]: {input.select_season()}"
    # @render.text
    # def track():
    #     return f"Selected [Track ID]: {input.select_track()}"
    # @render.text
    # def team():
    #     return f"Selected [Team ID]: {input.select_team()}"
    # @render.text
    # def driver():
    #     return f"Selected [Driver ID]: {input.select_driver()}"

# Content for each Question page
with ui.nav_panel("Question 1"):
    ui.h4("Which teams have dominated throughout time and how their performances varied?")
    with ui.layout_columns():
        with ui.card(full_screen=True):
            ui.card_header("Constructor Performance Over the Years")
            @render_plotly
            def constructor_performance():
                return plot_constructor_performance(total_points_for_sel_constructors())
            @render_plotly
            def top_10_teams():
                return plot_top_10_teams(constructor_top_10_average_points)


with ui.nav_panel("Question 2"):
    ui.h4("How have drivers performances evolved over time, and which drivers had the most consistent performance across seasons?")
    with ui.layout_columns():
        with ui.card(full_screen=True):
            ui.card_header("Driver Performance Over the Years")
            @render_plotly
            def driver_performance():
                return plot_driver_performance(total_points_for_sel_drivers())
            @render_plotly
            def top_10_drivers():
                return plot_top_10_drivers(driver_top_10_average_points)

with ui.nav_panel("Question 3"):
    ui.h4("How have pit stop timings and strategies affected race outcomes?")
    with ui.layout_columns():
        with ui.card(full_screen=True):
            ui.card_header("Average Pit Stop Duration per Race")
            @render_plotly
            def avg_pit_stops_graph():
                # Pass the relevant dataset to the function
                return avg_pit_stop_duration(q3_super_filter(q3_dataframes['pit_stop_records']))
            
            @render_plotly
            def bubble_cart_wins():
                # Pass the relevant dataset to the function
                return bubble_chart_wins_vs_pit_duration(q3_super_filter(q3_dataframes['pit_stop_records']))
            
            @render_plotly
            def scatter_times_and_wins():
                # Pass the relevant dataset to the function
                return scatter_wins_vs_pit_times(q3_dataframes['pit_stop_records'], q3_data_filter())
            
            @render_plotly
            def hist_of_laps():
                # Pass the relevant dataset to the function
                return histogram_pit_stop_laps(q3_track_filter(basic_pits))
            
            


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
    with ui.layout_columns(col_widths={"sm": (6,6,6,6)}):
        with ui.card(full_screen=True):
            ui.card_header("Number of drivers per constructor team")
            @render_plotly
            def drivers_per_constructor_q5():
                return drivers_per_team_barchart_q5(drivers_per_team_bar_data_q5())
        with ui.card(full_screen=True):
            ui.card_header("Total of points by driver")
            @render_plotly
            def points_per_driver_q5():
                return points_per_driver_barchart_q5(points_per_driver_bar_data_q5())
        with ui.card(full_screen=True):
            ui.card_header("Most completed races by driver")
            @render_plotly
            def completed_per_driver_q5():
                return races_per_driver_barchart_q5(races_per_driver_bar_data_q5())
        with ui.card(full_screen=True):
            ui.card_header("Summary of races per driver")
            @render.data_frame
            def races_summary_q5():
                return render.DataGrid(summary_data_q5(), styles=[{"style": {"font-size": "0.8em"}}])



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

# State variables - Store variables selected by the user
# Link: https://shiny.posit.co/py/docs/reactive-foundations.html#values
input_seasons = reactive.value(tuple())
input_teams = reactive.value(tuple())
input_drivers = reactive.value(tuple())
input_tracks = reactive.value(tuple())

@reactive.effect
@reactive.event(input.select_season, input.select_team, input.select_driver, input.select_track)
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
    # [1] Seasons filtering
    selected_seasons_lst: list[str] = []
    for item in selected_season_tuple:
        selected_seasons_lst.append(item)
    tmp_seasons_lst = tmp_lst[['year']]
    # Compare old selected "seasons" vs new selected "seasons"
    if selected_season_tuple != input_seasons():
        # user edit "season" select box = modified search = do not filter choices
        ui.update_selectize("select_season", choices=seasons_dict, selected=selected_seasons_lst)
        # Update "seasons" state variable with new values
        input_seasons.set(input_seasons() + selected_season_tuple)
    else:
        # user did not edit "season" select box = did not modified search = filter choices based on other boxes selection
        new_seasons_dict = update_dict(seasons_dict, tmp_seasons_lst.values, "season")
        ui.update_selectize("select_season", choices=new_seasons_dict, selected=selected_seasons_lst)
    # [2] Track filtering
    selected_tracks_lst: list[int] = []
    for item in selected_track_tuple:
        selected_tracks_lst.append(int(item))
    tmp_tracks_lst = tmp_lst[['circuitId']]
    # Compare old selected "tracks" vs new selected "tracks"
    if selected_track_tuple != input_tracks():
        # user edit "tracks" select box = modified search = do not filter choices
        ui.update_selectize("select_track", choices=tracks_dict, selected=selected_tracks_lst)
        # Update "tracks" state variable with new values
        input_tracks.set(input_tracks() + selected_track_tuple)
    else:
        # user did not edit "tracks" select box = did not modified search = filter choices based on other boxes selection
        new_tracks_dict = update_dict(tracks_dict, tmp_tracks_lst.values)
        ui.update_selectize("select_track", choices=new_tracks_dict, selected=selected_tracks_lst)
    # [3] Constructors filtering
    selected_teams_lst: list[int] = []
    for item in selected_team_tuple:
        selected_teams_lst.append(int(item))
    tmp_teams_lst = tmp_lst[['constructorId']]
    # Compare old selected "teams" vs new selected "teams"
    if selected_team_tuple != input_teams():
        # user edit "teams" select box = modified search = do not filter choices
        ui.update_selectize("select_team", choices=teams_dict, selected=selected_teams_lst)
        # Update "teams" state variable with new values
        input_teams.set(input_teams() + selected_team_tuple)
    else:
        # user did not edit "teams" select box = did not modified search = filter choices based on other boxes selection
        new_teams_dict = update_dict(teams_dict, tmp_teams_lst.values)
        ui.update_selectize("select_team", choices=new_teams_dict, selected=selected_teams_lst)
    # [4] Drivers filtering
    selected_drivers_lst: list[int] = []
    for item in selected_driver_tuple:
        selected_drivers_lst.append(int(item))
    tmp_drivers_lst = tmp_lst[['driverId']]
    # Compare old selected "drivers" vs new selected "drivers"
    if selected_driver_tuple != input_drivers():
        # user edit "drivers" select box = modified search = do not filter choices
        ui.update_selectize("select_driver", choices=drivers_dict, selected=selected_drivers_lst)
        # Update "drivers" state variable with new values
        input_drivers.set(input_drivers() + selected_driver_tuple)
    else:
        # user did not edit "drivers" select box = did not modified search = filter choices based on other boxes selection
        new_drivers_dict = update_dict(drivers_dict, tmp_drivers_lst.values)
        ui.update_selectize("select_driver", choices=new_drivers_dict, selected=selected_drivers_lst)

@reactive.effect
@reactive.event(input.reset)
def _():
    input_seasons.set(tuple())
    ui.update_selectize("select_season", choices=seasons_dict)
    input_teams.set(tuple())
    ui.update_selectize("select_team", choices=teams_dict)
    input_drivers.set(tuple())
    ui.update_selectize("select_driver", choices=drivers_dict)
    input_drivers.set(tuple())
    ui.update_selectize("select_track", choices=tracks_dict)



# Reactive calculation and effects for Questions 1 and 2
# Author: Siham Argaw
# --------------------------------------------------------

# Reactive function that triggers depending if an input variable changes (season - select box)
# Link: https://shiny.posit.co/py/api/express/reactive.calc.html
# @reactive.calc
# def drivers_per_sel_season():
#     # Get the selected season by the end user
#     selected_season_tuple: tuple = input.select_season()
#     # Filter the race list to only 2 columns: raceId and year
#     lst_races = race_schedule_df[['raceId', 'year']]
#     # If a season was chosen in the select box
#     if len(selected_season_tuple) > 0:
#         if selected_season_tuple[0] is not None:
#             # From the select box, get the selected years in a list
#             selected_season_lst: list[int] = []
#             for item in selected_season_tuple:
#                 selected_season_lst.append(seasons_dict[int(item)])
#             # Filter the drivers data by the selected seasons
#             lst_races = lst_races[lst_races['year'].isin(selected_season_lst)]
#     # Group the race list by the 'year' and count the number of 'raceId' per 'year'
#     lst_races = lst_races.groupby('year').count().reset_index()
#     return lst_races

## Write your functions for Q1 and Q2 here
@reactive.calc
def total_points_for_sel_constructors():
    # Get the selected team(s) by the end user
    selected_team_tuple: tuple = input.select_team()
    # If any teams are selected by user filter df
    if len(selected_team_tuple) > 0 and selected_team_tuple[0] is not None:
        selected_teams_lst = [teams_dict[int(team_id)] for team_id in selected_team_tuple]
        filtered_data = constructor_average_points_per_year[constructor_average_points_per_year['name'].isin(selected_teams_lst)]
    else:
        # If no team is selected, use the entire dataset
        filtered_data = constructor_average_points_per_year
    return filtered_data

@reactive.calc
def total_points_for_sel_drivers():
    # Get the selected driver(s) by the end user
    selected_driver_tuple: tuple = input.select_driver()
    # If any teams are selected by user filter df
    if len(selected_driver_tuple) > 0 and selected_driver_tuple[0] is not None:
        selected_drivers_lst = [drivers_dict[int(team_id)] for team_id in selected_driver_tuple]
        filtered_data = driver_average_points_per_year[driver_average_points_per_year ['name'].isin(selected_drivers_lst)]
    else:
        # If no team is selected, use the entire dataset
        filtered_data = driver_average_points_per_year
    return filtered_data

# Reactive calculation and effects for Question 3
# Author: Matthew Bush
# --------------------------------------------------------
## Write your functions for Q3 here
# How have pit stop Umings and strategies affected race outcomes?


@reactive.calc
def q3_data_filter():

    # Get the selected driver(s) by the end user
    selected_driver_tuple: tuple = input.select_driver()
    # If any teams are selected by user filter df
    if len(selected_driver_tuple) > 0 and selected_driver_tuple[0] is not None:
        selected_drivers_lst = [drivers_dict[int(team_id)] for team_id in selected_driver_tuple]
        filtered_data = q3_dataframes['pit_stop_records'][q3_dataframes['pit_stop_records'] ['name'].isin(selected_drivers_lst)]
    else:
        # If no team is selected, use the entire dataset
        filtered_data = q3_dataframes['pit_stop_records']
    
    return filtered_data

def q3_driver_filter(data):

    # Get the selected driver(s) by the end user
    selected_driver_tuple: tuple = input.select_driver()
    # If any teams are selected by user filter df
    if len(selected_driver_tuple) > 0 and selected_driver_tuple[0] is not None:
        selected_drivers_lst = [drivers_dict[int(team_id)] for team_id in selected_driver_tuple]
        filtered_data = data[data ['name'].isin(selected_drivers_lst)]
    else:
        # If no team is selected, use the entire dataset
        filtered_data = data
    
    return filtered_data


def q3_track_filter(data):
    selected_track_tuple: tuple = input.select_track()

    if len(selected_track_tuple) > 0 and selected_track_tuple[0] is not None:
        tracks = [int(track_id) for track_id in selected_track_tuple]
        filtered_data = data[data ['circuitId'].isin(tracks)]
    else:
        # If no team is selected, use the entire dataset
        filtered_data = data

    return filtered_data

def q3_super_filter(data):
    selected_track_tuple: tuple = input.select_track()

    if len(selected_track_tuple) > 0 and selected_track_tuple[0] is not None:
        tracks = [int(track_id) for track_id in selected_track_tuple]
        filtered_data = data[data ['circuitId'].isin(tracks)]

    else:
        # If no team is selected, use the entire dataset
        filtered_data = data   

    # Get the selected driver(s) by the end user
    selected_driver_tuple: tuple = input.select_driver()
    # If any teams are selected by user filter df
    if len(selected_driver_tuple) > 0 and selected_driver_tuple[0] is not None:
        selected_drivers_lst = [drivers_dict[int(team_id)] for team_id in selected_driver_tuple]
        filtered_data = filtered_data[filtered_data ['name'].isin(selected_drivers_lst)]
    
    return filtered_data
    


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

def standardize_status_label(in_status: str) -> str:
    # Set w/ unique status that tells if the driver completed the race
    finished_status_lst = {"Finished", "+1 Lap", "+2 Laps", "+3 Laps", "+4 Laps", "+5 Laps", "+6 Laps", "+7 Laps", "+8 Laps", "+9 Laps", "+10 Laps", "+11 Laps", "+12 Laps", "+13 Laps", "+14 Laps", "+15 Laps", "+16 Laps", "+17 Laps", "+18 Laps", "+19 Laps", "+20 Laps", "+21 Laps", "+22 Laps", "+23 Laps", "+24 Laps", "+25 Laps", "+26 Laps", "+29 Laps", "+30 Laps", "+38 Laps", "+42 Laps", "+44 Laps", "+46 Laps", "+49 Laps"}
    if in_status not in finished_status_lst:
        return "Not Finished"
    else:
        return "Finished"

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
    lst_data['Status'] = lst_data['Status'].apply(standardize_status_label)
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
    summary_data = summary_data[['year', 'Team', 'Driver', 'Track', 'Sprint_Pts', 'Qualifying_Pos', 'Race_Pts', 'Status']]
    return summary_data

# Question 5 methods
def make_name_shorter(in_name: str) -> str:
    if len(in_name) > 14:
        return in_name[:13] + ".."
    else:
        return in_name

@reactive.calc
def drivers_per_team_bar_data_q5():
    selected_team_tuple: tuple = input.select_team()
    selected_driver_tuple: tuple = input.select_driver()
    lst_data = _qualipos_racepts_df[['driverId','constructorId', 'Team']]
    lst_data = lst_data.drop_duplicates()
    lst_data = filter_df_by_selection(lst_data, selected_team_tuple, "team")
    lst_data = filter_df_by_selection(lst_data, selected_driver_tuple, "driver")
    # Count the drivers per Team
    lst_data = lst_data[['Team', 'driverId']]
    lst_data = lst_data.groupby('Team').count().reset_index()
    lst_data = lst_data.sort_values('driverId', ascending=False)
    lst_data['Team'] = lst_data['Team'].apply(make_name_shorter)
    return lst_data

@reactive.calc
def points_per_driver_bar_data_q5():
    selected_season_tuple: tuple = input.select_season()
    selected_track_tuple: tuple = input.select_track()
    selected_team_tuple: tuple = input.select_team()
    selected_driver_tuple: tuple = input.select_driver()
    lst_data = _qualipos_racepts_df[['raceId','year','circuitId','driverId','constructorId', 'Race_Pts', 'Driver']]
    lst_data = filter_df_by_selection(lst_data, selected_season_tuple, "season")
    lst_data = filter_df_by_selection(lst_data, selected_track_tuple, "track")
    lst_data = filter_df_by_selection(lst_data, selected_team_tuple, "team")
    lst_data = filter_df_by_selection(lst_data, selected_driver_tuple, "driver")
    # Add up the number of points by driver
    lst_data = lst_data[['Driver', 'Race_Pts']]
    lst_data = lst_data.groupby('Driver').sum().reset_index()
    lst_data = lst_data.sort_values('Race_Pts', ascending=False)
    lst_data['Driver'] = lst_data['Driver'].apply(make_name_shorter)
    return lst_data

def determine_type_status(in_status: str) -> int:
    if in_status == "Finished":
        return 1
    else:
        return 0

@reactive.calc
def races_per_driver_bar_data_q5():
    selected_season_tuple: tuple = input.select_season()
    selected_track_tuple: tuple = input.select_track()
    selected_team_tuple: tuple = input.select_team()
    selected_driver_tuple: tuple = input.select_driver()
    lst_data = _qualipos_racepts_df[['raceId','year','circuitId','driverId','constructorId', 'Driver', 'Status', 'Total status']]
    lst_data = filter_df_by_selection(lst_data, selected_season_tuple, "season")
    lst_data = filter_df_by_selection(lst_data, selected_track_tuple, "track")
    lst_data = filter_df_by_selection(lst_data, selected_team_tuple, "team")
    lst_data = filter_df_by_selection(lst_data, selected_driver_tuple, "driver")
    lst_data = lst_data[['Driver', 'Status', 'Total status']]
    # Create "Finished" field to set if the race was finished or not, based on the "Status" field
    lst_data['Finished'] = lst_data['Status'].apply(determine_type_status)
    lst_data_finished = lst_data[['Driver', 'Finished']].groupby('Driver').sum().reset_index()
    lst_data_total = lst_data[['Driver', 'Total status']].groupby('Driver').sum().reset_index()
    lst_data_all = lst_data_total.join(lst_data_finished.set_index('Driver'), on='Driver')
    lst_data_all.rename(columns={'Total status': 'Total'}, inplace=True)
    lst_data_all['RatioFinished'] = lst_data_all['Finished'] / lst_data_all['Total']
    lst_data_all['RatioFinished'] = lst_data_all['RatioFinished'].round(2)
    lst_data_all = lst_data_all.sort_values('RatioFinished', ascending=False)
    lst_data_all['Driver'] = lst_data_all['Driver'].apply(make_name_shorter)
    return lst_data_all

@reactive.calc
def summary_data_q5():
    selected_season_tuple: tuple = input.select_season()
    selected_track_tuple: tuple = input.select_track()
    selected_team_tuple: tuple = input.select_team()
    selected_driver_tuple: tuple = input.select_driver()
    summary_data = _qualipos_racepts_df.copy()
    summary_data = filter_df_by_selection(summary_data, selected_season_tuple, "season")
    summary_data = filter_df_by_selection(summary_data, selected_track_tuple, "track")
    summary_data = filter_df_by_selection(summary_data, selected_team_tuple, "team")
    summary_data = filter_df_by_selection(summary_data, selected_driver_tuple, "driver")
    summary_data = summary_data[['year', 'Team', 'Driver', 'Track', 'Race_Pts', 'Status']]
    return summary_data
