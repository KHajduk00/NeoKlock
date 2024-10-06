import time
import requests
from ascii_art import Colors, get_ascii_weather_icon, generate_time_display
from data_logger import format_weather_data, format_air_quality_data
from utilities import load_config, clear_screen, get_current_time

class WeatherStation:
    def __init__(self):
        config = load_config()
        self.api_key = config['API_KEY']
        self.city = config['CITY']
        self.weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={self.api_key}&units=metric'
        self.geo_url = f'http://api.openweathermap.org/geo/1.0/direct?q={self.city}&limit=1&appid={self.api_key}'

    def get_weather_data(self):
        """Fetch weather data from OpenWeatherMap API."""
        try:
            response = requests.get(self.weather_url)
            response.raise_for_status()
            data = response.json()

            return {
                'weather_icon': data['weather'][0]['icon'],
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'visibility': data['visibility'],
                'wind_speed': data['wind']['speed'],
                'clouds': data['clouds']['all'],
                'rain': data['rain']['1h'] if 'rain' in data else "No Data",
                'lat': data['coord']['lat'],
                'lon': data['coord']['lon']
            }
        except requests.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None

    def get_air_quality(self, lat, lon):
        """Fetch air quality data from OpenWeatherMap API."""
        air_quality_url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={self.api_key}'
        try:
            response = requests.get(air_quality_url)
            response.raise_for_status()
            data = response.json()
            return data['list'][0]['main']['aqi'], data['list'][0]['components']
        except requests.RequestException as e:
            print(f"Error fetching air quality data: {e}")
            return None, None

    def display_weather_dashboard(self):
        """Display weather dashboard with continuous updates."""
        while True:
            clear_screen()
            current_time = get_current_time()

            # Display time
            time_display = generate_time_display(current_time)
            for row in time_display:
                print(Colors.BOLD + Colors.GREEN + row + Colors.RESET)

            # Get and display weather data
            weather_data = self.get_weather_data()
            if weather_data:
                weather_icon = get_ascii_weather_icon(weather_data['weather_icon'])
                print(f"\nWeather: {weather_icon}")

                # Display weather information
                for line in format_weather_data(weather_data, self.city):
                    print(line)

                # Get and display air quality
                aqi_index, components = self.get_air_quality(weather_data['lat'], weather_data['lon'])
                for line in format_air_quality_data(aqi_index, components):
                    print(line)

            time.sleep(60)  # Update every minute

def main():
    weather_station = WeatherStation()
    weather_station.display_weather_dashboard()

if __name__ == "__main__":
    main()
