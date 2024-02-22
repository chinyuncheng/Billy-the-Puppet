from utils import game_session

async def list_command(message):
    game_sessions = game_session.load_game_sessions()

    session_list = [f'{name} - {session["time"]}' for name, session in game_sessions.items()]

    if session_list:
        await message.channel.send('Scheduled game sessions:')
        await message.channel.send('\n'.join(session_list))
    else:
        await message.channel.send('No scheduled game sessions found.')
