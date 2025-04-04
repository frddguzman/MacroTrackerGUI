
import FreeSimpleGUI as sg
import csv
import os

MACRO_FILE = 'user_macros.csv'

def calculate_bmr(weight, height, age, sex):
    if sex == 'm':
        return 10 * weight + 6.25 * height - 5 * age + 5
    else:
        return 10 * weight + 6.25 * height - 5 * age - 161

def get_activity_multiplier(level):
    levels = {
        'Sedentary': 1.2,
        'Light': 1.375,
        'Moderate': 1.55,
        'Active': 1.725,
        'Very Active': 1.9
    }
    return levels.get(level, 1.55)

def adjust_goal(tdee, label):
    goals = {
        'High Deficit': 0.8,
        'Medium Deficit': 0.85,
        'Low Deficit': 0.9,
        'Maintenance': 1.0,
        'Hypertrophy': 1.1
    }
    return tdee * goals.get(label, 1.0)

def set_macro_goals_window():
    layout = [
        [sg.Text("Set Your Macros (Auto Calculation)")],
        [sg.Text("Weight (kg):"), sg.Input(key='weight')],
        [sg.Text("Height (cm):"), sg.Input(key='height')],
        [sg.Text("Age:"), sg.Input(key='age')],
        [sg.Text("Sex:"), sg.Combo(['Male', 'Female'], key='sex')],
        [sg.Text("Activity Level:"), sg.Combo(
            ['Sedentary', 'Light', 'Moderate', 'Active', 'Very Active'],
            default_value='Moderate', key='activity')],
        [sg.Text("Goal:"), sg.Combo(
            ['High Deficit', 'Medium Deficit', 'Low Deficit', 'Maintenance', 'Hypertrophy'],
            default_value='Maintenance', key='goal')],
        [sg.Button("Calculate & Save"), sg.Button("Cancel")]
    ]

    window = sg.Window("Macro Goal Setup", layout, modal=True)

    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, "Cancel"):
            break
        elif event == "Calculate & Save":
            try:
                if not values['weight'] or not values['height'] or not values['age'] or not values['sex']:
                    raise ValueError("⚠️ Please complete all required fields.")
                weight = float(values['weight'])
                height = float(values['height'])
                age = int(values['age'])
                sex_input = values['sex']
                if sex_input not in ['Male', 'Female']:
                    raise ValueError("Please select 'Male' or 'Female'.")
                sex = 'm' if sex_input == 'Male' else 'f'
                activity = values['activity']
                goal_label = values['goal']

                bmr = calculate_bmr(weight, height, age, sex)
                multiplier = get_activity_multiplier(activity)
                tdee = bmr * multiplier
                adjusted_calories = adjust_goal(tdee, goal_label)

                protein_per_kg = 2 if "Hypertrophy" in goal_label else 1.5
                protein = protein_per_kg * weight
                protein_cal = protein * 4
                fat = (adjusted_calories * 0.25) / 9
                carbs = (adjusted_calories - (protein_cal + fat * 9)) / 4

                with open(MACRO_FILE, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['calories', 'protein', 'carbs', 'fat'])
                    writer.writerow([round(adjusted_calories), round(protein), round(carbs), round(fat)])

                sg.popup("✅ Macro goals calculated and saved successfully!", f"Calories: {round(adjusted_calories)} kcal", f"Protein: {round(protein)} g", f"Carbs: {round(carbs)} g", f"Fat: {round(fat)} g")
                break

            except ValueError as ve:
                sg.popup_error(str(ve))
            except Exception as e:
                sg.popup_error("Error calculating macros.", str(e))

    window.close()

if __name__ == "__main__":
    set_macro_goals_window()
