import config
import datetime
import pytz
from utils.datetime_helper import get_time
from utils.json_helper import save_game_sessions, load_game_sessions
from utils.game_session_message import update_message

async def host_command(message):
    """
    Host a game session.
    """
    content = message.content.replace('host ', '')
    parts = content.split(',')

    name = ''
    player = 0
    date = ''
    endtime = 0
    timezone = None

    for part in parts:
        if '=' in part:
            param_name, param_value = part.split('=')
            param_value = param_value.strip()

            if param_name == 'name':
                name = param_value
            elif param_name == 'player':
                player = int(param_value)
            elif param_name == 'date':
                date = param_value
            elif param_name == 'endtime':
                endtime = int(param_value)
            elif param_name == 'timezone':
                timezone = param_value

    if not name or player <= 0 or not date or endtime <= 0:
        await message.channel.send('Please provide name, player (as a positive integer), date, and endtime (as a positive integer) after the `host` command.')
        return
    
    try:
        date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M')
    except ValueError:
        await message.channel.send('Please provide date in the format "YYYY-MM-DD HH:MM".')
        return
    
    if timezone is None:
        timezone = pytz.timezone(config.TIMEZONE)
    else:
        try:
            timezone = pytz.timezone(timezone)
        except Exception as e:
            await message.channel.send("Please refer to the website for all available timezone: https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568")

    now = get_time(specific_timezone=timezone)
    game_sessions = load_game_sessions()

    key = f'{name}_{now.strftime("%Y%m%d%H%M%S")}'

    author = {
        message.author.id : message.author.display_name
    }

    game_sessions[key] = {
        'name': name,
        'player': player,
        'date': date.isoformat(),
        'endtime': endtime,
        'created_by': author,
        'created_at': now.isoformat(),
        'message_id': '',
        'timezone': timezone.zone,
        'participants': {},
    }

    response_message_content = 'Received'
    response_message = await message.channel.send(response_message_content)
    game_sessions[key]['message_id'] = response_message.id

    save_game_sessions(game_sessions)

    try:
        updated_message_content = await update_message(game_sessions[key])
        await response_message.edit(content=updated_message_content)
    except Exception as e:
        await message.channel.send("An error occurred while updating the game session details. Please try again later.")
