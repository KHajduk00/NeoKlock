# Weather and Air Quality Logger

This application fetches and displays current weather and air quality data for a specified city. It logs the data into a CSV file and provides a visual representation of the current time and weather conditions.

## Features

- Real-time display of current time in a 7-segment display format
- Fetches and displays current weather data including temperature, humidity, pressure, visibility, wind speed, cloud coverage, and rainfall
- Retrieves and shows air quality index (AQI) and detailed pollutant concentrations
- Logs weather and air quality data to a CSV file hourly
- Displays weather condition using ASCII art icons
- Continuous updating of displayed information

## Requirements

- Python 3.6+
- `requests` library
- OpenWeatherMap API key

## Installation

1. Clone this repository or download the script.
2. Install the required Python library:

   ```
   pip install requests
   ```

## Configuration

Before running the application, you need to create a `config.json` file in the same directory as the script. This file should contain your OpenWeatherMap API key and the city you want to monitor:

```json
{
  "API_KEY": "your_openweathermap_api_key_here",
  "CITY": "Your City Name"
}
```

Replace `"your_openweathermap_api_key_here"` with your actual OpenWeatherMap API key, and `"Your City Name"` with the name of the city you want to monitor.

## Usage

Run the script using Python:

```
python weather_logger.py
```

The application will start displaying the current time and updating weather and air quality information every minute. Data is logged to a CSV file (named after your city) every hour.

## CSV Output

The application generates a CSV file named after your specified city (e.g., `YourCity.csv`). This file contains hourly logs of weather and air quality data, including:

- Timestamp
- Temperature
- Feels like temperature
- Humidity
- Pressure
- Visibility
- Wind speed
- Cloud coverage
- Rainfall
- Air Quality Index (AQI)
- Concentrations of various pollutants (CO, NO, NO2, O3, SO2, PM2.5, PM10, NH3)

This data can be used for further analysis or visualization using other tools.

## Note

This application requires an active internet connection to fetch real-time data from the OpenWeatherMap API.
