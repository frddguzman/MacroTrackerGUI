import FreeSimpleGUI as sg
import matplotlib
matplotlib.use('TkAgg')  # Abre la ventana de Matplotlib normal
import matplotlib.pyplot as plt
import csv
import os
from datetime import datetime

def show_macro_history():
    # 1. Verificar si existe daily_logs.csv
    if not os.path.exists('daily_logs.csv'):
        sg.popup("No history found (daily_logs.csv not found).")
        return

    # 2. Cargar datos
    with open('daily_logs.csv', mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        data = list(reader)

    # 3. Verificar si hay registros
    if not data:
        sg.popup("daily_logs.csv is empty.")
        return

    # 4. Extraer fechas y calorías
    dates = [row['date'] for row in data]
    cals = [float(row['cal']) for row in data]

    # 5. Crear figura y trazar la gráfica
    plt.figure()
    plt.plot(dates, cals, marker='o')
    plt.title('Daily Calories Over Time')
    plt.xlabel('Date')
    plt.ylabel('Calories')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # 6. Después de cerrar el gráfico, preguntar si deseas guardar como PNG
    if sg.popup_yes_no("Do you want to save this chart as PNG?") == 'Yes':
        filename = f"calories_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(filename)
        sg.popup(f"Chart saved as {filename}!")

# Ejecución directa (para pruebas)
if __name__ == "__main__":
    show_macro_history()
