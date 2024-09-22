# -*- coding: utf-8 -*-

import os
import time
import requests
import csv
from datetime import datetime
import json

# Load the configuration file
with open('config.json') as config_file:
    config = json.load(config_file)

# Access API_KEY and CITY
API_KEY = config['API_KEY']
CITY = config['CITY']

WEATHER_URL = f'http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric'
GEO_URL = f'http://api.openweathermap.org/geo/1.0/direct?q={CITY}&limit=1&appid={API_KEY}'

# Function to display ASCII art for weather icons
def get_ascii_weather_icon(icon_code):
    weather_icons = {
        "01d": "☀️",  # Clear sky (day)
        "01n": "🌙",  # Clear sky (night)
        "02d": "⛅",  # Few clouds (day)
        "02n": "🌑",  # Few clouds (night)
        "03d": "☁️",  # Scattered clouds
        "03n": "☁️",
        "04d": "☁️",  # Broken clouds
        "04n": "☁️",
        "09d": "🌧️",  # Shower rain
        "09n": "🌧️",
        "10d": "🌦️",  # Rain (day)
        "10n": "🌧️",  # Rain (night)
        "11d": "⛈️",  # Thunderstorm
        "11n": "⛈️",
        "13d": "❄️",  # Snow
        "13n": "❄️",
        "50d": "🌫️",  # Mist
        "50n": "🌫️"
    }
    return weather_icons.get(icon_code, "❓")  # Default to a question mark if icon not found

# Correct mapping of digits to their corresponding 7-segment display form using 'l' and '_'
digit_map = {
    '0': [" _ ", "l l", "l_l"],
    '1': ["   ", "  l", "  l"],
    '2': [" _ ", " _l", "l_ "],
    '3': [" _ ", " _l", " _l"],
    '4': ["   ", "l_l", "  l"],
    '5': [" _ ", "l_ ", " _l"],
    '6': [" _ ", "l_ ", "l_l"],
    '7': [" _ ", "  l", "  l"],
    '8': [" _ ", "l_l", "l_l"],
    '9': [" _ ", "l_l", " _l"]
}

# Mapping of Qualitative names for aqi index numbers
aqi_index_map = {
    '1': "(Good)",
    '2': "(Fair)",
    '3': "(Moderate)",
    '4': "(Poor)",
    '5': "(Very Poor)"
}

# Function to get latitude and longitude based on city
def get_lat_lon():
    try:
        response = requests.get(GEO_URL)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        if data:
            lat = data[0]['lat']
            lon = data[0]['lon']
            return lat, lon
        else:
            return None, None  # No data returned
    except requests.RequestException as e:
        print(f"Error fetching geocoding data: {e}")
        return None, None  # If API call fails, return None

# Function to get weather data (temperature, rain, wind, etc.) using the city name
def get_weather_data():
    try:
        response = requests.get(WEATHER_URL)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        # Extracting all required fields
        weather_icon = data['weather'][0]['icon']
        temperature = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        visibility = data['visibility']
        wind_speed = data['wind']['speed']
        clouds = data['clouds']['all']
        rain = data['rain']['1h'] if 'rain' in data else "No Data"  # Rain data may not always be available

        lat = data['coord']['lat']
        lon = data['coord']['lon']

        return {
            'weather_icon': weather_icon,
            'temperature': temperature,
            'feels_like': feels_like,
            'humidity': humidity,
            'pressure': pressure,
            'visibility': visibility,
            'wind_speed': wind_speed,
            'clouds': clouds,
            'rain': rain,
            'lat': lat,
            'lon': lon
        }
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None  # If API call fails, return None

# Function to get air quality data based on latitude and longitude
def get_air_quality(lat, lon):
    AIR_QUALITY_URL = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}'
    try:
        response = requests.get(AIR_QUALITY_URL)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        # Extract air quality index and components
        air_quality_index = data['list'][0]['main']['aqi']
        components = data['list'][0]['components']

        return air_quality_index, components
    except requests.RequestException as e:
        print(f"Error fetching air quality data: {e}")
        return None, None

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class Colors:
    GREEN = '\033[92m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def log_data_to_csv(city, weather_data, air_quality_index, components):
    filename = f"{city}.csv"
    now = datetime.now()
    time_str = now.strftime("%Y-%m-%d %H:%M:%S")

    # Data to write
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

def display_time_and_weather():
    last_logged_time = time.time() - 3600  # Start with an hour ago to ensure initial logging

    while True:
        clear_screen()

        # Get current time (only hours and minutes)
        current_time = time.strftime("%H:%M")

        # Print the time in 7-segment format
        rows = ["", "", ""]
        for char in current_time:
            if char == ':':  # Handle the colon separately
                rows[0] += "   "
                rows[1] += " . "
                rows[2] += " . "
            else:
                rows[0] += digit_map[char][0] + " "
                rows[1] += digit_map[char][1] + " "
                rows[2] += digit_map[char][2] + " "

        for row in rows:
            print(Colors.BOLD + Colors.GREEN + row + Colors.RESET)

        # Fetch and log weather data every hour
        current_time_epoch = time.time()
        if current_time_epoch - last_logged_time >= 3600:
            last_logged_time = current_time_epoch
            weather_data = get_weather_data()
            if weather_data is not None:
                lat = weather_data['lat']
                lon = weather_data['lon']
                weather_icon = get_ascii_weather_icon(weather_data['weather_icon'])
                air_quality_index, components = get_air_quality(lat, lon)

                # Log data to CSV
                if air_quality_index is not None and components is not None:
                    log_data_to_csv(CITY, weather_data, air_quality_index, components)
            else:
                print("Could not retrieve weather data.")

        # Display weather icon
        if weather_data is not None:
            print(f"\nWeather: {get_ascii_weather_icon(weather_data['weather_icon'])}")

            # Display weather data if available
            print(f"\nCurrent temperature in {CITY}: {weather_data['temperature']}°C (Feels like: {weather_data['feels_like']}°C)")
            print(f"Humidity: {weather_data['humidity']}%")
            print(f"Pressure: {weather_data['pressure']} hPa")
            print(f"Visibility: {weather_data['visibility']} meters")
            print(f"Wind speed: {weather_data['wind_speed']} m/s")
            print(f"Clouds: {weather_data['clouds']}%")
            print(f"Rain (last 1 hour): {weather_data['rain']} mm")

            # Display air quality if available
            if air_quality_index is not None and components is not None:
                aqi_description = aqi_index_map.get(str(air_quality_index), "(Unknown)")

                print(f"\nAir Quality Index (AQI): {air_quality_index} {aqi_description}")
                print(f"CO: {components['co']} μg/m³")
                print(f"NO: {components['no']} μg/m³")
                print(f"NO2: {components['no2']} μg/m³")
                print(f"O3: {components['o3']} μg/m³")
                print(f"SO2: {components['so2']} μg/m³")
                print(f"PM2.5: {components['pm2_5']} μg/m³")
                print(f"PM10: {components['pm10']} μg/m³")
                print(f"NH3: {components['nh3']} μg/m³")
        else:
            print("\nCould not retrieve weather data.")

        time.sleep(60)  # Refresh every 60 seconds

# Fetch initial weather data
weather_data = get_weather_data()
if weather_data is not None:
    lat = weather_data['lat']
    lon = weather_data['lon']
    air_quality_index, components = get_air_quality(lat, lon)
    if air_quality_index is not None and components is not None:
        log_data_to_csv(CITY, weather_data, air_quality_index, components)

# Run the clock with weather and air quality display
display_time_and_weather()
