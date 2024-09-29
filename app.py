import time
from utilities import clear_screen, Colors
from weather import get_weather_data, get_air_quality
from ascii_art import display_time
from data_logger import log_data_to_csv
import json

# Load the configuration file
with open('config.json') as config_file:
    config = json.load(config_file)

CITY = config['CITY']

def display_time_and_weather():
    last_logged_time = time.time() - 3600  # Start with an hour ago to ensure initial logging

    while True:
        clear_screen()

        # Display current time in 7-segment format
        current_time = time.strftime("%H:%M")
        display_time(current_time)

        # Fetch and log weather data every hour
        current_time_epoch = time.time()
        if current_time_epoch - last_logged_time >= 3600:
            last_logged_time = current_time_epoch
            weather_data = get_weather_data(CITY)
            if weather_data:
                lat = weather_data['lat']
                lon = weather_data['lon']
                air_quality_index, components = get_air_quality(lat, lon)

                if air_quality_index is not None and components is not None:
                    log_data_to_csv(CITY, weather_data, air_quality_index, components)

        time.sleep(60)  # Refresh every 60 seconds

# Run the clock with weather and air quality display
display_time_and_weather()
