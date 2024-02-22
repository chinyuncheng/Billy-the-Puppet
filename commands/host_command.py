import datetime
import pytz
from utils.game_session import save_game_sessions, load_game_sessions
from utils.update_message import update_message

async def host_command(message, client):
    """
    Host a game session.
    """
    content = message.content.replace('host ', '')
    parts = content.split(',')

    name = ''
    players = 0
    scheduled_time = ''
    recruitment_end_time = ''

    for part in parts:
        if '=' in part:
            param_name, param_value = part.split('=')

            param_value = param_value.strip()

            if param_name == 'name':
                name = param_value
            elif param_name == 'players':
                players = int(param_value)
            elif param_name == 'scheduled_time':
                scheduled_time = param_value
            elif param_name == 'recruitment_end_time':
                recruitment_end_time = param_value

    if not name or players <= 0 or not scheduled_time or not recruitment_end_time:
        await message.channel.send('Please provide name, players (as a positive integer), scheduled_time, and recruitment_end_time after the `host` command.')
        return
    
    try:
        scheduled_time = datetime.datetime.strptime(scheduled_time, '%Y-%m-%d %H:%M')
        recruitment_end_time = datetime.datetime.strptime(recruitment_end_time, '%Y-%m-%d %H:%M')
    except ValueError:
        await message.channel.send('Please provide scheduled_time and recruitment_end_time in the format "YYYY-MM-DD HH:MM".')
        return

    local_timezone = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
    if local_timezone != pytz.timezone('Asia/Taipei').localize(datetime.datetime.now()).tzinfo:
        scheduled_time = pytz.timezone('Asia/Taipei').localize(scheduled_time)
        recruitment_end_time = pytz.timezone('Asia/Taipei').localize(recruitment_end_time)

    game_sessions = load_game_sessions()

    author = message.author.display_name
    now = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
    key = f'{name}_{author}_{now}'

    game_sessions[key] = {
        'name': name,
        'players': players,
        'scheduled_time': scheduled_time.isoformat(),
        'recruitment_end_time': recruitment_end_time.isoformat(),
        'created_by': author,
        'created_at': now,
        'participants': [author]
    }

    save_game_sessions(game_sessions)

    initial_message_content = await update_message(game_sessions[key])
    initial_message = await message.channel.send(initial_message_content)

    def check(reaction, user):
        return user != client.user and str(reaction.emoji) == '✅'

    reaction, user = await client.wait_for('reaction_add', check=check)

    game_sessions[key]['participants'].append(user.display_name)
    save_game_sessions(game_sessions)
    await message.channel.send(f'{user.display_name} has joined the game session.')

    updated_message_content = await update_message(game_sessions[key])
    await initial_message.edit(content=updated_message_content)
