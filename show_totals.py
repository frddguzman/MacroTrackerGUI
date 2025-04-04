
import FreeSimpleGUI as sg
import csv
from datetime import datetime

LOG_FILE = 'daily_logs.csv'

def load_today_totals():
    today = datetime.now().strftime('%Y-%m-%d')
    try:
        with open(LOG_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['date'] == today:
                    return row
    except FileNotFoundError:
        return None
    return None

def show_totals_window():
    today_totals = load_today_totals()
    if not today_totals:
        sg.popup("No logged macros for today.", title="Today's Totals")
        return

    layout = [
        [sg.Text(f"Macros for {today_totals['date']}")],
        [sg.Text(f"Calories: {today_totals['cal']} kcal")],
        [sg.Text(f"Protein: {today_totals['protein']} g")],
        [sg.Text(f"Carbs: {today_totals['carbs']} g")],
        [sg.Text(f"Fiber: {today_totals['fiber']} g")],
        [sg.Text(f"Net Carbs: {today_totals['net_carbs']} g")],
        [sg.Text(f"Sugar: {today_totals['sugar']} g")],
        [sg.Text(f"Total Fat: {today_totals['total_fat']} g")],
        [sg.Button("Close")]
    ]

    window = sg.Window("Today's Macros", layout, modal=True)
    while True:
        event, _ = window.read()
        if event in (sg.WINDOW_CLOSED, "Close"):
            break
    window.close()

if __name__ == "__main__":
    show_totals_window()
