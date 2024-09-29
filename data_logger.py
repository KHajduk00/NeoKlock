import csv
from datetime import datetime
import os

def log_data_to_csv(city, weather_data, air_quality_index, components):
    filename = f"{city}.csv"
    now = datetime.now()
    time_str = now.strftime("%Y-%m-%d %H:%M:%S")

    data = {
        'Time': time_str,
        'Temperature': weather_data['temperature'],
        'Feels Like': weather_data['feels_like'],
        'Humidity': weather_data['humidity'],
        'Pressure': weather_data['pressure'],
        'Visibility': weather_data['visibility'],
        'Wind Speed': weather_data['wind_speed'],
        'Clouds': weather_data['clouds'],
        'Rain': weather_data['rain'],
        'AQI': air_quality_index,
        'CO': components['co'],
        'NO': components['no'],
        'NO2': components['no2'],
        'O3': components['o3'],
        'SO2': components['so2'],
        'PM2.5': components['pm2_5'],
        'PM10': components['pm10'],
        'NH3': components['nh3']
    }

    file_exists = os.path.isfile(filename)

    with open(filename, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)
