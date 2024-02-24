import config
import json

def save(data, path=config.GAME_EVENTS_FILE_PATH):
    """
    Save data to a JSON file.
    """
    with open(path, 'w') as file:
        json.dump(data, file)

def load(path=config.GAME_EVENTS_FILE_PATH):
    """
    Load data from a JSON file.
    """
    try:
        with open(path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}
    return data
