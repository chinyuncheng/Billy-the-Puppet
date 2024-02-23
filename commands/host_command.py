import datetime
import pytz
from utils.json_helper import save_game_sessions, load_game_sessions
from utils.game_session_message import update_message

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

    now = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
    key = f'{name}_{now}'

    author = {
        message.author.id : message.author.display_name
    }

    game_sessions[key] = {
        'name': name,
        'players': players,
        'scheduled_time': scheduled_time.isoformat(),
        'recruitment_end_time': recruitment_end_time.isoformat(),
        'created_by': author,
        'created_at': now,
        'participants': {},
    }

    save_game_sessions(game_sessions)

    initial_message_content = await update_message(game_sessions[key])
    initial_message = await message.channel.send(initial_message_content)
    
    async def on_raw_reaction_add(payload):
        if payload.member.bot:
            return

        if payload.message_id == initial_message.id and payload.user_id not in game_sessions[key]['participants'].keys():
            user = await client.fetch_user(payload.user_id)
            game_sessions[key]['participants'][user.id] = user.display_name
            save_game_sessions(game_sessions)
            updated_message_content = await update_message(game_sessions[key])
            await initial_message.edit(content=updated_message_content)

    async def on_raw_reaction_remove(payload):
        if payload.message_id == initial_message.id and payload.user_id in game_sessions[key]['participants']:
            del game_sessions[key]['participants'][payload.user_id]
            save_game_sessions(game_sessions)
            updated_message_content = await update_message(game_sessions[key])
            await initial_message.edit(content=updated_message_content)
    
    client.event(on_raw_reaction_add)
    client.event(on_raw_reaction_remove)
