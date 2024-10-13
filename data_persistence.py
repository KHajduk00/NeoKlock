import csv
from datetime import datetime
from pathlib import Path
import logging
from utilities import load_config

logger = logging.getLogger('WeatherStation.DataPersistence')

def get_city_name():
    """Get the city name from the config file."""
    config = load_config()
    return config['CITY'].replace(' ', '_').lower()

def initialize_csv(city):
    """Create data directory and city-specific CSV file with headers if they don't exist."""
    data_dir = Path('data')
    data_dir.mkdir(exist_ok=True)

    csv_file = data_dir / f'{city}_weather_data.csv'

    if not csv_file.exists():
        headers = [
            'Time', 'Temperature', 'Feels Like', 'Humidity', 'Pressure',
            'Visibility', 'Wind Speed', 'Clouds', 'Rain', 'AQI',
            'CO', 'NO', 'NO2', 'O3', 'SO2', 'PM2.5', 'PM10', 'NH3'
        ]

        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)

    return csv_file

def save_data(weather_data, aqi_index, components):
    """Save weather and air quality data to city-specific CSV file."""
    try:
        city = get_city_name()
        csv_file = initialize_csv(city)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        row = [
            timestamp,
            weather_data['temperature'],
            weather_data['feels_like'],
            weather_data['humidity'],
            weather_data['pressure'],
            weather_data['visibility'],
            weather_data['wind_speed'],
            weather_data['clouds'],
            weather_data['rain'],
            aqi_index,
            components['co'],
            components['no'],
            components['no2'],
            components['o3'],
            components['so2'],
            components['pm2_5'],
            components['pm10'],
            components['nh3']
        ]

        with open(csv_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(row)

        logger.debug(f"Data saved successfully for {city} at {timestamp}")

    except Exception as e:
        logger.error(f"Error saving data: {str(e)}")

def get_latest_data():
    """Retrieve the most recent data entry for the configured city."""
    try:
        city = get_city_name()
        csv_file = initialize_csv(city)
        with open(csv_file, 'r') as f:
            for row in reversed(list(csv.reader(f))):
                if row and row[0] != 'Time':  # Skip header
                    return {
                        'timestamp': row[0],
                        'weather': {
                            'temperature': float(row[1]),
                            'feels_like': float(row[2]),
                            'humidity': int(row[3]),
                            'pressure': int(row[4]),
                            'visibility': int(row[5]),
                            'wind_speed': float(row[6]),
                            'clouds': int(row[7]),
                            'rain': row[8]
                        },
                        'air_quality': {
                            'aqi': int(row[9]),
                            'components': {
                                'co': float(row[10]),
                                'no': float(row[11]),
                                'no2': float(row[12]),
                                'o3': float(row[13]),
                                'so2': float(row[14]),
                                'pm2_5': float(row[15]),
                                'pm10': float(row[16]),
                                'nh3': float(row[17])
                            }
                        }
                    }
    except Exception as e:
        logger.error(f"Error retrieving latest data: {str(e)}")
        return None
