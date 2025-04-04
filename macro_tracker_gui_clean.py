
import FreeSimpleGUI as sg
from add_meal_advanced import add_meal_window
from show_totals import show_totals_window
from show_ingredient_list import show_ingredient_list_window
from set_macro_goals import set_macro_goals_window
from macro_history import show_macro_history


sg.theme('DarkGreen5')

def load_user_macros():
    try:
        with open("user_macros.csv", mode='r') as file:
            import csv
            reader = csv.DictReader(file)
            for row in reader:
                return {
                    'calories': float(row['calories']),
                    'protein': float(row['protein'])
                }
    except:
        return None

def load_today_macros():
    from datetime import datetime
    try:
        with open("daily_logs.csv", mode='r') as file:
            import csv
            reader = csv.DictReader(file)
            today = datetime.now().strftime('%Y-%m-%d')
            for row in reader:
                if row['date'] == today:
                    return {
                        'cal': float(row['cal']),
                        'protein': float(row['protein'])
                    }
    except:
        return None

def update_macro_status(window):
    today = load_today_macros()
    goals = load_user_macros()
    if not today or not goals:
        window['macro_status'].update("No data available.")
        return

    summary = (
        f"Calories: {round(today['cal'], 2)} / {goals['calories']} kcal\n"
        f"Protein:  {round(today['protein'], 2)} / {goals['protein']} g"
    )
    window['macro_status'].update(summary)

left_column = [
    [sg.Text('Macro Tracker 500 - GUI Edition', font=('Helvetica', 16), justification='center')],
    [sg.Button('Add Meal', size=(25, 1))],
    [sg.Button("View Today's Totals", size=(25, 1))],
    [sg.Button('Macro History', size=(25, 1))],
    [sg.Button('Ingredient List', size=(25, 1))],
    [sg.Button('Set Macro Goals', size=(25, 1))],
    [sg.Button('Exit', size=(25, 1))]
]

right_column = [
    [sg.Text('Daily Summary (Calories & Protein)', font=('Helvetica', 12))],
    [sg.Multiline('', size=(30, 8), key='macro_status', disabled=True)]
]

layout = [
    [
        sg.Column(left_column),
        sg.VSeperator(),
        sg.Column(right_column)
    ]
]

window = sg.Window('Macro Tracker 500', layout, finalize=True)
update_macro_status(window)

while True:
    event, _ = window.read()
    if event in (sg.WINDOW_CLOSED, 'Exit'):
        break
    elif event == 'Add Meal':
        add_meal_window()
        update_macro_status(window)
    elif event == "View Today's Totals":
        show_totals_window()
    elif event == 'Ingredient List':
        show_ingredient_list_window()
        update_macro_status(window)
    elif event == 'Set Macro Goals':
        set_macro_goals_window()
        update_macro_status(window)
    elif event == 'Macro History':
        show_macro_history()


window.close()
