import json

JSON_FILE_PATH = 'game_sessions.json'

def save_game_sessions(game_sessions):
    """Save game session data to a JSON file."""
    with open(JSON_FILE_PATH, 'w') as file:
        json.dump(game_sessions, file)

def load_game_sessions():
    """Load game session data from a JSON file."""
    try:
        with open(JSON_FILE_PATH, 'r') as file:
            game_sessions = json.load(file)
    except FileNotFoundError:
        game_sessions = {}
    return game_sessions

