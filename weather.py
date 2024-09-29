import requests
import json

with open('config.json') as config_file:
    config = json.load(config_file)

API_KEY = config['API_KEY']

def get_weather_data(city):
    WEATHER_URL = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    try:
        response = requests.get(WEATHER_URL)
        response.raise_for_status()
        data = response.json()

        weather_data = {
            'weather_icon': data['weather'][0]['icon'],
            'temperature': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'visibility': data['visibility'],
            'wind_speed': data['wind']['speed'],
            'clouds': data['clouds']['all'],
            'rain': data.get('rain', {}).get('1h', "No Data"),
            'lat': data['coord']['lat'],
            'lon': data['coord']['lon']
        }

        return weather_data
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

def get_air_quality(lat, lon):
    AIR_QUALITY_URL = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}'
    try:
        response = requests.get(AIR_QUALITY_URL)
        response.raise_for_status()
        data = response.json()
        air_quality_index = data['list'][0]['main']['aqi']
        components = data['list'][0]['components']
        return air_quality_index, components
    except requests.RequestException as e:
        print(f"Error fetching air quality data: {e}")
        return None, None
