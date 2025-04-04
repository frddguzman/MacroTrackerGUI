import FreeSimpleGUI as sg
DB_FILE = 'ingredients_detailed.csv'
import csv

import os
from datetime import datetime

LOG_FILE = 'daily_logs.csv'
LOG_FIELDS = ['date', 'cal', 'protein', 'carbs', 'fiber', 'sugar', 'net_carbs', 'saturated_fat', 'unsaturated_fat', 'total_fat']



def log_named_meal(meal_name, macros):
    today = datetime.now().strftime('%Y-%m-%d')
    meal_log = 'named_meal_log.csv'
    fields = ['date', 'meal_name'] + [k for k in LOG_FIELDS if k != 'date']
    rows = []

    if os.path.exists(meal_log):
        with open(meal_log, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if not (row['date'] == today and row['meal_name'] == meal_name):
                    rows.append(row)

    new_entry = {'date': today, 'meal_name': meal_name}
    new_entry.update({k: round(macros.get(k, 0), 2) for k in LOG_FIELDS if k != 'date'})
    rows.append(new_entry)

    with open(meal_log, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    log_today_macros(macros)
    meal_log = 'named_meal_log.csv'
    fields = ['date', 'meal_name'] + [k for k in LOG_FIELDS if k != 'date']
    rows = []
    log_today_macros(macros)

    if os.path.exists(meal_log):
        with open(meal_log, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if not (row['date'] == today and row['meal_name'] == meal_name):
                    rows.append(row)

    new_entry = {'date': today, 'meal_name': meal_name}
    new_entry.update({k: round(macros.get(k, 0), 2) for k in LOG_FIELDS if k != 'date'})
    rows.append(new_entry)

    with open(meal_log, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    today = datetime.now().strftime('%Y-%m-%d')
    meal_log = 'named_meal_log.csv'
    if not os.path.exists(meal_log):
        with open(meal_log, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['date', 'meal_name'])
    temp = []
    with open(meal_log, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            if not (row[0] == today and row[1] == meal_name):
                temp.append(row)
    temp.append([today, meal_name])
    with open(meal_log, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['date', 'meal_name'])
        writer.writerows(temp)


def get_today_meal_names():
    today = datetime.now().strftime('%Y-%m-%d')
    meal_log = 'named_meal_log.csv'
    if not os.path.exists(meal_log):
        return []
    with open(meal_log, 'r') as file:
        reader = csv.DictReader(file)
        return [row['meal_name'] for row in reader if row['date'] == today]







def log_today_macros(macros):
    today = datetime.now().strftime('%Y-%m-%d')
    meal_log = 'named_meal_log.csv'
    if not os.path.exists(meal_log):
        return

    latest_meals = {}
    with open(meal_log, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['date'] == today:
                latest_meals[row['meal_name']] = row

    daily_macros = {k: 0 for k in LOG_FIELDS if k != 'date'}
    for meal in latest_meals.values():
        for k in daily_macros:
            daily_macros[k] += float(meal.get(k, 0))

    logs = {}
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                logs[row['date']] = row

    logs[today] = {'date': today, **{k: round(daily_macros[k], 2) for k in daily_macros}}

    with open(LOG_FILE, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=LOG_FIELDS)
        writer.writeheader()
        writer.writerows(logs.values())
    meal_log = 'named_meal_log.csv'
    if not os.path.exists(meal_log):
        return

    latest_meals = {}
    with open(meal_log, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['date'] == today:
                latest_meals[row['meal_name']] = row  # overwrite by meal name

    # Accumulate from latest entries only
    daily_macros = {k: 0 for k in LOG_FIELDS if k != 'date'}
    for meal in latest_meals.values():
        for k in daily_macros:
            daily_macros[k] += float(meal.get(k, 0))

    # Overwrite today's entry in daily_logs.csv
    logs = {}
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                logs[row['date']] = row

    logs[today] = {'date': today, **{k: round(daily_macros[k], 2) for k in daily_macros}}

    with open(LOG_FILE, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=LOG_FIELDS)
        writer.writeheader()
        writer.writerows(logs.values())
    today = datetime.now().strftime('%Y-%m-%d')
    meal_log = 'named_meal_log.csv'
    if not os.path.exists(meal_log):
        return

    latest_meals = {}
    with open(meal_log, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['date'] == today:
                latest_meals[row['meal_name']] = row  # overwrite by meal name

    # Accumulate from latest entries only
    daily_macros = {k: 0 for k in LOG_FIELDS if k != 'date'}
    for meal in latest_meals.values():
        for k in daily_macros:
            daily_macros[k] += float(meal.get(k, 0))

    # Overwrite today's entry in daily_logs.csv
    logs = {}
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                logs[row['date']] = row

    logs[today] = {'date': today, **{k: round(daily_macros[k], 2) for k in daily_macros}}

    with open(LOG_FILE, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=LOG_FIELDS)
        writer.writeheader()
        writer.writerows(logs.values())


def calculate_meal(meal_dict):
    macros = {
        'cal': 0, 'protein': 0, 'carbs': 0, 'fiber': 0, 'sugar': 0,
        'net_carbs': 0, 'saturated_fat': 0, 'unsaturated_fat': 0, 'total_fat': 0
    }
    try:
        with open(DB_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            db = {row['ingredient']: row for row in reader}

        for item, grams in meal_dict.items():
            if item in db:
                factor = grams / 100
                macros['cal'] += float(db[item]['calories']) * factor
                macros['protein'] += float(db[item]['protein']) * factor
                macros['carbs'] += float(db[item]['carbs']) * factor
                macros['fiber'] += float(db[item]['fiber']) * factor
                macros['sugar'] += float(db[item]['sugar']) * factor
                macros['saturated_fat'] += float(db[item]['saturated_fat']) * factor
                macros['unsaturated_fat'] += float(db[item]['unsaturated_fat']) * factor
            else:
                sg.popup_error(f"Ingredient '{item}' not found in database.")
        macros['net_carbs'] = macros['carbs'] - macros['fiber']
        macros['total_fat'] = macros['saturated_fat'] + macros['unsaturated_fat']
        return macros
    except Exception as e:
        sg.popup_error("Error calculating macros.", str(e))
        return {key: 0 for key in ['cal', 'protein', 'carbs', 'fiber', 'sugar', 'net_carbs', 'saturated_fat', 'unsaturated_fat', 'total_fat']}


def load_ingredients():
    try:
        with open(DB_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            return [row['ingredient'] for row in reader]
    except Exception as e:
        sg.popup_error("Failed to load ingredients database.", str(e))
        return []

def add_meal_window():
    ingredients = load_ingredients()
    if not ingredients:
        return

    meal_items = []

    layout = [
        [sg.Text("Meal Name:"), sg.Input(key='meal_name')],
        [sg.Text("Search Ingredient:"), sg.Input(enable_events=True, key='search_input')],
        [sg.Listbox(values=[], size=(40, 5), key='suggestions', enable_events=True)],
        [sg.Button("Add Ingredient"), sg.Button("Remove Selected")],
        [sg.Listbox(values=[], key='ingredient_list', size=(40, 6))],
        [sg.Frame('Current Macros', [[sg.Multiline('', size=(40, 6), key='macro_summary', disabled=True)]])],
        [sg.Text('Meals Logged Today:'), sg.Text('', key='meal_log_display', size=(40, 1))],
        [sg.Button("Save Meal"), sg.Button("Cancel")]
    ]

    window = sg.Window("Add Meal", layout, modal=True, finalize=True)
    window['meal_log_display'].update(', '.join(get_today_meal_names()))

    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, "Cancel"):
            break

        # Live update suggestion list
        elif event == 'search_input':
            query = values['search_input'].lower()
            matches = [i for i in ingredients if query in i.lower()]
            window['suggestions'].update(matches)

        # Add ingredient from listbox selection
        elif event == 'suggestions':
            selected = values['suggestions'][0]
            try:
                grams = float(sg.popup_get_text(f"How many grams of '{selected}'?", title="Grams"))
                meal_items.append((selected, grams))
                window['ingredient_list'].update([f"{name}: {grams}g" for name, grams in meal_items])

                meal_dict = {name: grams for name, grams in meal_items}
                macros = calculate_meal(meal_dict)
                summary = "\n".join([
                    f"Calories: {round(macros['cal'], 2)} kcal",
                    f"Protein: {round(macros['protein'], 2)} g",
                    f"Carbs: {round(macros['carbs'], 2)} g",
                    f"Fiber: {round(macros['fiber'], 2)} g",
                    f"Net Carbs: {round(macros['net_carbs'], 2)} g",
                    f"Fat: {round(macros['total_fat'], 2)} g"
                ])
                window['macro_summary'].update(summary)


                meal_dict = {name: grams for name, grams in meal_items}
                macros = calculate_meal(meal_dict)
                summary = "\n".join([
                    f"Calories: {round(macros['cal'], 2)} kcal",
                    f"Protein: {round(macros['protein'], 2)} g",
                    f"Carbs: {round(macros['carbs'], 2)} g",
                    f"Fiber: {round(macros['fiber'], 2)} g",
                    f"Net Carbs: {round(macros['net_carbs'], 2)} g",
                    f"Fat: {round(macros['total_fat'], 2)} g"
                ])
                window['macro_summary'].update(summary)

                window['search_input'].update('')
                window['suggestions'].update([])
            except (ValueError, TypeError):
                sg.popup_error("Please enter a valid number.")

        # Remove selected from added ingredients
        elif event == "Remove Selected":
            to_remove = values['ingredient_list']
            if to_remove:
                for item in to_remove:
                    name = item.split(":")[0].strip()
                    meal_items = [entry for entry in meal_items if entry[0] != name]
                window['ingredient_list'].update([f"{name}: {grams}g" for name, grams in meal_items])

                meal_dict = {name: grams for name, grams in meal_items}
                macros = calculate_meal(meal_dict)
                summary = "\n".join([
                    f"Calories: {round(macros['cal'], 2)} kcal",
                    f"Protein: {round(macros['protein'], 2)} g",
                    f"Carbs: {round(macros['carbs'], 2)} g",
                    f"Fiber: {round(macros['fiber'], 2)} g",
                    f"Net Carbs: {round(macros['net_carbs'], 2)} g",
                    f"Fat: {round(macros['total_fat'], 2)} g"
                ])
                window['macro_summary'].update(summary)


        # Save meal
        elif event == "Save Meal":
            if not values['meal_name'] or not meal_items:
                sg.popup_error("Meal name and at least one ingredient are required.")
                continue
            meal_dict = {name: grams for name, grams in meal_items}
            macros = calculate_meal(meal_dict)
            log_today_macros(macros)
            log_named_meal(values['meal_name'], macros)
            meal_names = get_today_meal_names()
            window['meal_log_display'].update(', '.join(meal_names))
            sg.popup("✅ Meal Saved and Logged!", f"Name: {values['meal_name']}", "Ingredients:", *[f"{n}: {g}g" for n, g in meal_items])
            break

    window.close()

if __name__ == "__main__":
    add_meal_window()