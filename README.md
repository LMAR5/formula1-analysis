# Formula 1 Analysis

**Formula 1 Analysis** aims to explore historical trends in Formula 1 racing (1950–2024) through an interactive data visualization system by analyzing key factors such as team dominance, driver performance, and pit stop strategies. The project seeks to provide visually engaging insights for fans, analysts, and strategists.

Some key questions the system answers are:
- Which teams have dominated over the years, and how have their performances fluctuated?
- Which drivers have shown consistent performance across seasons?
- How have pit stop strategies influenced race outcomes?
- What is the impact of qualifying sessions and sprints on race performance?
- Which teams have nurtured the most talented drivers?

Furthermore, each question have its own view, that consists on a collection of charts (line, bar, bubble, histogram, etc.), which will highlight key trends, visualize correlations, and provide insights to address each key question.

## Dataset

Our dataset was obtained from Kaggle, and it captures over 7 decades of Formula 1 racing (1950-2024). 
It includes detailed data on races, drivers, teams, circuits, and more, offering insights into the Formula 1 sport.
Similarly, it's organized into multiple CSV files (comma as separator), where each file contains the list of drivers with their details, the list of circuits, all the race results with their timings per driver per team, all the race schedules across time, and more.

**Source**: https://www.kaggle.com/datasets/muhammadehsan02/formula-1-world-championship-history-1950-2024

## Team members

- Luis Aguilar (MS in CS at SFSU)
- Siham Argaw (MS in CS at SFSU)
- Matthew Bush (MS in Data Science and AI at SFSU)

## The application was built using

|  Category  |      Name      |                     Description                            |
| :--------: | :------------: | :--------------------------------------------------------- |
| Language   |    Python 3    | Main programming language                                  |
| Dependency |     Pandas     | To clean, explore, and manipulate data.                    |
| Dependency |     Plotly     | To generate interactive web-based visualizations.          |
| Dependency |     Shiny      | Framework to build interactive web apps only using Python. |
____________________________________________________________________________________________

## Application architecture

![Application architecture](https://github.com/LMAR5/formula1-analysis/blob/main/documentation/app_architecture.jpg)

## Getting started

### Prerequisites
- Install the latest version of Python 3 in your machine
- Install the latest version of VSCode in your machine

### Installation

1. Clone the repository
```
git clone https://github.com/LMAR5/formula1-analysis.git
```
2. Go into the new directory
```
cd formula1-analysis
```
3. Create a virtual environment with the following command (will create a `.venv` directory):
- Note: Instead of relying and installing several system-wide Python libraries, we'll use an isolated virtual environment.
```
python3 -m venv .venv
```
4. Activate the virtual environment with the following command:
```
source .venv/bin/activate
```
5. To check if your virtual environment is activated, use the following command:
(If the virtual environment is activated, the command will output a filepath that includes the `.venv` directory)
```
which python
```
6. If you want deactivate the virtual environment (not needed right now), run the following command:
```
deactivate
```
7. Install dependencies from the requirements.txt file
```
pip install -r requirements.txt
```
8. Run the Shiny app with the following command:
`--reload` will reload the app anytime you save changes in your Python file. `--launch-browser` will automatically open your browser.
```
shiny run --reload --launch-browser app.py
```
9. The app should be running on `http://127.0.0.1:8000/`

### Troubleshooting

At VSCode, if you get the `report missing imports` from Pylance (error message) check the following link:

- Link: https://stackoverflow.com/a/71918838

You'll have to create the `.vscode` directory, create a `settings.json` file, and add the `python.defaultInterpreterPath` property so VSCode can find the dependencies from your Python path.

## App Screenshots

### Question 1 view

- **Question**: Which teams have dominated over the years, and how have their performances fluctuated?
- **Visualizations to answer the question**:
  - Line chart - Performance of Formula 1 drivers over time
  - Bar chart - Rank top 10 teams based on average points scored

![Question 1 view](https://github.com/luisaguilar159/fa24-csc805-g4-f1/blob/main/screenshots/question1.jpg)

### Question 2 view

- **Question**: Which drivers have shown consistent performance across seasons?
- **Visualizations to answer the question**:
  - Line chart - Performance trends over time
  - Rank top 10 drivers based on points scored

![Question 2 view](https://github.com/luisaguilar159/fa24-csc805-g4-f1/blob/main/screenshots/question2.jpg)

### Question 3 view

- **Question**: How have pit stop strategies influenced race outcomes?
- **Visualizations to answer the question**:
  - Bar chart - Drivers' average pit stop times
  - Bubble chart - Wins, Avg. Pit Stop times, and Total Stops
  - Histogram - Distribution of timing of pit stops

![Question 3 view](https://github.com/luisaguilar159/fa24-csc805-g4-f1/blob/main/screenshots/question3.jpg)

### Question 4 view

- **Question**: What is the impact of qualifying sessions and sprints on race performance?
- **Visualizations to answer the question**:
  - Bubble chart - Qualifying position vs Race points
  - Bubble chart - Sprint points vs Race points
  - Pie chart - Status of races by Driver
  - Table - Summary of races by Driver

![Question 4 view](https://github.com/luisaguilar159/fa24-csc805-g4-f1/blob/main/screenshots/question4.jpg)

### Question 5 view

- **Question**: Which teams have nurtured the most talented drivers?
- **Visualizations to answer the question**:
  - Bar chart - Number of drivers by Constructor team
  - Bar chart - Total points by Driver
  - Bar chart - Most completed races by Driver
  - Table - Summary of races by Driver

![Question 5 view](https://github.com/luisaguilar159/fa24-csc805-g4-f1/blob/main/screenshots/question5.jpg)
