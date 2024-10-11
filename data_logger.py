from datetime import datetime
from ascii_art import Colors

AQI_INDEX_MAP = {
    '1': "(Good)",
    '2': "(Fair)",
    '3': "(Moderate)",
    '4': "(Poor)",
    '5': "(Very Poor)"
}

def get_temp_color(temp):
        if int(temp) >= 25:
            return Colors.RED
        elif int(temp) in range(15, 25):
            return Colors.YELLOW
        else:
            return Colors.BLUE

def format_weather_data(weather_data, city):
    """Format weather data for display."""
    if weather_data is None:
        return ["Could not retrieve weather data."]

    temp_color = get_temp_color(weather_data['temperature'])
    feels_like_color = get_temp_color(weather_data['feels_like'])

    lines = [
        f"\nCurrent temperature in {city}: " + temp_color + f"{weather_data['temperature']}°C " + Colors.RESET + f"(Feels like: " + feels_like_color + f"{weather_data['feels_like']}°C" + Colors.RESET + ")",
        f"Humidity: {weather_data['humidity']}%",
        f"Pressure: {weather_data['pressure']} hPa",
        f"Visibility: {weather_data['visibility']} meters",
        f"Wind speed: {weather_data['wind_speed']} m/s",
        f"Clouds: {weather_data['clouds']}%",
        f"Rain (last 1 hour): {weather_data['rain']} mm"
    ]
    return lines

def format_air_quality_data(aqi_index, components):
    """Format air quality data for display."""
    if aqi_index is None or components is None:
        return ["Could not retrieve air quality data."]

    aqi_description = AQI_INDEX_MAP.get(str(aqi_index), "(Unknown)")
    lines = [
        f"\nAir Quality Index (AQI): {aqi_index} {aqi_description}",
        f"CO: {components['co']} μg/m³",
        f"NO: {components['no']} μg/m³",
        f"NO2: {components['no2']} μg/m³",
        f"O3: {components['o3']} μg/m³",
        f"SO2: {components['so2']} μg/m³",
        f"PM2.5: {components['pm2_5']} μg/m³",
        f"PM10: {components['pm10']} μg/m³",
        f"NH3: {components['nh3']} μg/m³"
    ]
    return lines
