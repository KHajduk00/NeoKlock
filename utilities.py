import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class Colors:
    GREEN = '\033[92m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
