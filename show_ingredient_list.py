
import FreeSimpleGUI as sg
import csv

DB_FILE = 'ingredients_detailed.csv'


def add_ingredient_form(window):
    layout = [
        [sg.Text("Ingredient Name:"), sg.Input(key='name')],
        [sg.Text("Calories per 100g:"), sg.Input(key='calories')],
        [sg.Text("Protein (g):"), sg.Input(key='protein')],
        [sg.Text("Carbs (g):"), sg.Input(key='carbs')],
        [sg.Text("Fiber (g):"), sg.Input(key='fiber')],
        [sg.Text("Sugar (g):"), sg.Input(key='sugar')],
        [sg.Text("Saturated Fat (g):"), sg.Input(key='sat_fat')],
        [sg.Text("Unsaturated Fat (g):"), sg.Input(key='unsat_fat')],
        [sg.Button("Save"), sg.Button("Cancel")]
    ]

    form = sg.Window("Add New Ingredient", layout, modal=True)
    while True:
        event, values = form.read()
        if event in (sg.WINDOW_CLOSED, "Cancel"):
            form.close()
            break
        elif event == "Save":
            try:
                name = values['name'].strip()
                if not name:
                    raise ValueError("Name is required.")
                new_row = [
                    name,
                    float(values['calories']),
                    float(values['protein']),
                    float(values['carbs']),
                    float(values['fiber']),
                    float(values['sugar']),
                    float(values['sat_fat']),
                    float(values['unsat_fat']),
                ]
                with open(DB_FILE, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(new_row)
                sg.popup("✅ Ingredient added successfully.")
                form.close()
                window['ingredient_display'].update(load_ingredient_names())
                break
            except Exception as e:
                sg.popup_error("Failed to save ingredient:", str(e))

def load_ingredient_names():
    try:
        with open(DB_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            return [row['ingredient'] for row in reader]
    except:
        return []


def show_ingredient_list_window():
    try:
        with open(DB_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            ingredients = [row['ingredient'] for row in reader]
    except Exception as e:
        sg.popup_error("Failed to load ingredient list.", str(e))
        return

    if not ingredients:
        sg.popup("No ingredients found.")
        return

    layout = [
        [sg.Text("Ingredient List:")],
        [sg.Listbox(values=ingredients, size=(40, 15), key='ingredient_display')],
        [sg.Button("Add Ingredient"), sg.Button("Close")]
    ]

    window = sg.Window("Ingredient List", layout, modal=True)
    while True:
        event, _ = window.read()
        if event == "Add Ingredient":
            add_ingredient_form(window)
        elif event in (sg.WINDOW_CLOSED, "Close"):
            break
    window.close()

if __name__ == "__main__":
    show_ingredient_list_window()
