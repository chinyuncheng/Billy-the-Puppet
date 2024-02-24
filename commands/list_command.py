from utils import json_helper

async def list_command(message):
    """
    List existing scheduled game events.
    """
    game_sessions = json_helper.load_game_sessions()

    session_list = [f'{name} - {session["time"]}' for name, session in game_sessions.items()]

    if session_list:
        await message.channel.send('Scheduled game sessions:')
        await message.channel.send('\n'.join(session_list))
    else:
        await message.channel.send('No scheduled game sessions found.')
