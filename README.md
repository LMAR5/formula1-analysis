# Formula 1 Analysis
Formula 1 Analysis is an interactive data visualization system that explores historical trends in Formula 1.

- Dataset link: https://www.kaggle.com/datasets/muhammadehsan02/formula-1-world-championship-history-1950-2024

## Team

Team 04:
- Luis Aguilar
- Siham Argaw
- Matthew Bush

## Getting started

### Prerequisites
- Have Python 3 installed in your local machine
- Have VSCode installed

### Installation

1. Clone the repository
```
git clone https://github.com/luisaguilar159/fa24-csc805-g4-f1.git
```
2. Go into the new directory
```
cd fa24-csc805-g4-f1
```
3. Create a virtual environment with the following command (will create a `.venv` directory):
- Instead of relying and installing several system-wide Python libraries, we'll use an isolated virtual environment.
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

### Question 1 charts

![Question 1 view](https://github.com/luisaguilar159/fa24-csc805-g4-f1/blob/main/screenshots/question1.jpg)

### Question 2 charts

![Question 2 view](https://github.com/luisaguilar159/fa24-csc805-g4-f1/blob/main/screenshots/question2.jpg)

### Question 3 charts

![Question 3 view](https://github.com/luisaguilar159/fa24-csc805-g4-f1/blob/main/screenshots/question3.jpg)

### Question 4 charts

![Question 4 view](https://github.com/luisaguilar159/fa24-csc805-g4-f1/blob/main/screenshots/question4.jpg)

### Question 5 charts

![Question 5 view](https://github.com/luisaguilar159/fa24-csc805-g4-f1/blob/main/screenshots/question5.jpg)
