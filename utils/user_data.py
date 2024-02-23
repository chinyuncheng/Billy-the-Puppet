import os
import requests
from dotenv import load_dotenv

def get_user_display_name(user_id):
    load_dotenv()

    TOKEN = os.getenv('DISCORD_BOT_TOKEN')

    headers = {
        'Authorization': f'Bot {TOKEN}'  # Replace 'Bot' with 'Bearer' if using an OAuth2 token
    }
    response = requests.get(f'https://discord.com/api/users/{user_id}', headers=headers)
    if response.status_code == 200:
        user_data = response.json()
        return user_data.get('global_name')
    else:
        print(f"Failed to fetch user data. Status code: {response.status_code}")
        return None
