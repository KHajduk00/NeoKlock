import os
import json
import time

def load_config(config_path='config.json'):
    """Load configuration from JSON file."""
    with open(config_path, 'r') as f:
        config = json.load(f)
    return config

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_current_time():
    """Get current time in HH:MM format."""
    return time.strftime("%H:%M")
