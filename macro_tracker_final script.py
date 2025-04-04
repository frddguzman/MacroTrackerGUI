
import csv
import os
import random
from datetime import datetime
import matplotlib.pyplot as plt

DB_FILE = 'ingredients_detailed.csv'
LOG_FILE = 'daily_logs.csv'
LOG_FIELDS = ['date', 'cal', 'protein', 'carbs', 'fiber', 'sugar', 'net_carbs', 'saturated_fat', 'unsaturated_fat', 'total_fat']
meals = {}

def ensure_ingredient_db_exists():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ingredient', 'calories', 'protein', 'carbs', 'fiber', 'sugar', 'saturated_fat', 'unsaturated_fat'])
        print("Created a new ingredients database. Start by adding your first ingredients.")


def get_choice(prompt, options):
    while True:
        val = input(prompt).strip().lower()
        if val in options:
            return val
        else:
            print(f"Invalid input. Please choose one of: {', '.join(options)}.")

def get_float(prompt):
    while True:
        val = input(prompt).strip()
        try:
            return float(val)
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

def add(name):
    print(f"Adding ingredient: {name}")
    cal = get_float("Calories per 100g: ")
    protein = get_float("Protein per 100g (g): ")
    carbs = get_float("Total Carbs per 100g (g): ")
    fiber = get_float("Fiber per 100g (g): ")
    sugar = get_float("Sugar per 100g (g): ")
    sat_fat = get_float("Saturated Fat per 100g (g): ")
    unsat_fat = get_float("Unsaturated Fat per 100g (g): ")

    with open(DB_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, cal, protein, carbs, fiber, sugar, sat_fat, unsat_fat])

    print(f"{name} added successfully.")

def calculate_meal(meal_dict):
    macros = {k: 0 for k in ['cal', 'protein', 'carbs', 'fiber', 'sugar', 'net_carbs', 'saturated_fat', 'unsaturated_fat', 'total_fat']}
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
            print(f"Ingredient '{item}' not found in database.")
            choice = input(f"Do you want to add '{item}' now? (y/n): ").strip().lower()
            if choice == 'y':
                add(item)
                return calculate_meal(meal_dict)
            else:
                print("Meal creation canceled due to missing ingredient.")
                return None
    macros['net_carbs'] = macros['carbs'] - macros['fiber']
    macros['total_fat'] = macros['saturated_fat'] + macros['unsaturated_fat']
    return macros

def print_macros(title, macros):
    print(f"\n{title} macros:")
    for k, v in macros.items():
        print(f"- {k}: {round(v, 2)}")

def sum_macros(*meals):
    total = {k: 0 for k in meals[0]}
    for meal in meals:
        for k, v in meal.items():
            total[k] += v
    return total

def load_user_macros():
    try:
        with open("user_macros.csv", mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                return {
                    'calories': float(row['calories']),
                    'protein': float(row['protein']),
                    'carbs': float(row['carbs']),
                    'fat': float(row['fat'])
                }
    except FileNotFoundError:
        print("No user macro target file found. Please run set.")
        return None

def compare_with_goals(total):
    print("\n--- Comparison with Your Daily Targets ---")
    goals = load_user_macros()
    if not goals:
        return

    for macro in ['calories', 'protein', 'carbs', 'fat']:
        actual = round(total.get('cal' if macro == 'calories' else macro, 0), 2)
        target = round(goals[macro], 2)
        diff = actual - target
        status = "over" if diff > 0 else "under"
        print(f"{macro.capitalize()}: {actual} vs {target} ({abs(round(diff, 2))} {status})")

def add_meal():
    tag = input("-> Name your meal (e.g., breakfast, lunch, dinner): ").strip().lower()
    entry = input("-> What did you eat? (e.g., chicken breast:150, avocado:100): ")
    items = [x.strip() for x in entry.split(',')]
    meal = {}
    for item in items:
        if ':' in item:
            name, grams = item.split(':')
            meal[name.strip()] = float(grams.strip())
    meal_data = calculate_meal(meal)
    if meal_data is None:
        return
    meals[tag] = meal_data
    print(f"Saved {tag}! :)")
    if input("-> Do you want to track your macros? (y/n): ").strip().lower() == 'y':
        print_macros(tag.capitalize(), meals[tag])
    if input("-> Do you want to know your total macros for today? (y/n): ").strip().lower() == 'y':
        show_total()

def list_ingredients():
    try:
        with open(DB_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            ingredients = [row['ingredient'] for row in reader]
        if not ingredients:
            print("No ingredients found in the database.")
            return
        choice = input("-> Display all ingredients? (y/n): ").strip().lower()
        display = ingredients if choice == 'y' else random.sample(ingredients, min(20, len(ingredients)))
        print("\nIngredients List:")
        for i, name in enumerate(display, 1):
            print(f"{i}. {name}")
    except Exception as e:
        print(f"Error reading ingredients: {e}")

def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100
    return weight / (height_m ** 2)

def calculate_bmr(weight, height, age, sex):
    if sex == 'm':
        return 10 * weight + 6.25 * height - 5 * age + 5
    else:
        return 10 * weight + 6.25 * height - 5 * age - 161

def get_activity_multiplier(level):
    return {
        'sedentary': 1.2, 'light': 1.375, 'moderate': 1.55, 'active': 1.725, 'very active': 1.9
    }.get(level.lower(), 1.55)

def adjust_goal(tdee, goal):
    return {
        'deficit_high': tdee * 0.8,
        'deficit_medium': tdee * 0.85,
        'deficit_low': tdee * 0.9,
        'hypertrophy': tdee * 1.1
    }.get(goal, tdee)

def set_macros():
    if os.path.exists("user_macros.csv"):
        with open("user_macros.csv", mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                print(f"Your current macros are: {row['calories']} kcal, {row['protein']}g protein, {row['carbs']}g carbs, {row['fat']}g fat")
                if input("Do you want to change them? (y/n): ").strip().lower() != 'y':
                    return

    print("Let's set up your daily macro targets.")
    weight = get_float("Enter your weight (kg): ")
    height = get_float("Enter your height (cm): ")
    age = int(get_float("Enter your age: "))
    sex = get_choice("Enter your sex (m/f): ", ["m", "f"])
    activity = get_choice("Activity level (sedentary/light/moderate/active/very active): ", ["sedentary", "light", "moderate", "active", "very active"])

    bmi = calculate_bmi(weight, height)
    bmr = calculate_bmr(weight, height, age, sex)
    tdee = bmr * get_activity_multiplier(activity)

    print(f"Your BMI is {round(bmi, 2)}")
    print(f"Your BMR is {round(bmr)} kcal/day")
    print(f"Your TDEE is approximately {round(tdee)} kcal/day")

    goal = get_choice("Goal? (deficit_high/deficit_medium/deficit_low/maintenance/hypertrophy): ", ["deficit_high", "deficit_medium", "deficit_low", "maintenance", "hypertrophy"])
    adjusted_calories = adjust_goal(tdee, goal)

    protein_per_kg = 2 if "hypertrophy" in goal else 1.5
    protein = protein_per_kg * weight
    protein_cal = protein * 4
    fat = (adjusted_calories * 0.25) / 9
    carbs = (adjusted_calories - (protein_cal + fat * 9)) / 4

    print(f"Calculated Macros for goal '{goal}':\nCalories: {round(adjusted_calories)} kcal\nProtein: {round(protein)} g\nCarbs: {round(carbs)} g\nFat: {round(fat)} g")

    with open("user_macros.csv", mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['calories', 'protein', 'carbs', 'fat'])
        writer.writerow([round(adjusted_calories), round(protein), round(carbs), round(fat)])
    print("Macros saved successfully!")

def log_today_macros(total):
    today = datetime.now().strftime('%Y-%m-%d')
    logs = {}
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                logs[row['date']] = row
    logs[today] = {**{'date': today}, **{k: round(total[k], 2) for k in total}}
    with open(LOG_FILE, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=LOG_FIELDS)
        writer.writeheader()
        writer.writerows(logs.values())
    print("✔️ Macros logged for today.")

def show_macro_history():
    if not os.path.exists(LOG_FILE):
        print("No macro log history found.")
        return
    with open(LOG_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        data = list(reader)
    if not data:
        print("Log file is empty.")
        return
    dates = [row['date'] for row in data]
    cal = [float(row['cal']) for row in data]
    protein = [float(row['protein']) for row in data]
    carbs = [float(row['carbs']) for row in data]
    fat = [float(row['total_fat']) for row in data]
    plt.plot(dates, cal, label='Calories')
    plt.plot(dates, protein, label='Protein')
    plt.plot(dates, carbs, label='Carbs')
    plt.plot(dates, fat, label='Fat')
    plt.xlabel('Date')
    plt.ylabel('Amount')
    plt.title('Macro History')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()
    if input("-> Would you like to save the graph as PNG? (y/n): ").strip().lower() == 'y':
        filename = f"macro_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(filename)
        print(f"Graph saved as {filename}")

def show_total():
    if meals:
        meal_names = ", ".join(meals.keys())
        print(f"\n-> Today you've eaten: {meal_names}")
        total = sum_macros(*meals.values())
        print_macros("Today's total", total)
        compare_with_goals(total)
        if input("-> Do you want to log your total macros? (y/n): ").strip().lower() == 'y':
            log_today_macros(total)
    else:
        print("No meals tracked yet.")

def main():
    ensure_ingredient_db_exists()
    print("Hello! How's it going? Macro Tracker 500 here :P")
    while True:
        print("\nWhat do you want to do?")
        print("-> add (add a meal or a new ingredient)")
        print("-> total (see today's total macros)")
        print("-> list (see the ingredients list)")
        print("-> set (view or change your macro goals)")
        print("-> history (see macro log history)")
        print("-> exit (to quit)")
        command = input("-> ").strip().lower()
        if command == 'add':
            what = input("What do you want to add, a meal or a new ingredient? ").strip().lower()
            if what == 'meal':
                add_meal()
            elif what == 'ingredient':
                name = input("Name of the ingredient: ").strip().lower()
                add(name)
            else:
                print("Invalid option.")
        elif command == 'total':
            show_total()
        elif command == 'list':
            list_ingredients()
        elif command == 'set':
            set_macros()
        elif command == 'history':
            show_macro_history()
        elif command == 'exit':
            if meals:
                if input("-> Do you want to log today's macros before exiting? (y/n): ").strip().lower() == 'y':
                    total = sum_macros(*meals.values())
                    log_today_macros(total)
            print("Goodbye! See you next meal :)")
            break
        else:
            print("Invalid command.")

if __name__ == '__main__':
    main()
