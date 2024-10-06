# ASCII art handling module
class Colors:
    GREEN = '\033[92m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

# Mapping for weather icons
WEATHER_ICONS = {
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

DIGIT_MAP = {
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

def get_ascii_weather_icon(icon_code):
    """Return ASCII weather icon based on icon code."""
    return WEATHER_ICONS.get(icon_code, "❓")

def generate_time_display(current_time):
    """Generate ASCII art representation of time."""
    rows = ["", "", ""]
    for char in current_time:
        if char == ':':
            rows[0] += "   "
            rows[1] += " . "
            rows[2] += " . "
        else:
            rows[0] += DIGIT_MAP[char][0] + " "
            rows[1] += DIGIT_MAP[char][1] + " "
            rows[2] += DIGIT_MAP[char][2] + " "
    return rows
#Test/Test