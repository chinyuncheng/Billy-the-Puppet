"""
MIT License

Copyright (c) 2024-present chinyuncheng

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import config
import datetime
import pytz
from core.game_events import GameEvent
from utils import datetime_helper, json_helper

# TODO: Add language feature
command_descriptions = {
    'host': 'Schedule a game event.',
    'list': 'List existing scheduled game events.'
}
command_usages = {
    'host': 'host <name>,<player>,<date>,<endtime (hrs)>,[timezone]',
    'list': 'list [-a] [-h]'
}
command_examples = {
    'host': 'host name=Baldur''s Gate 3,player=4,date=2024-02-25 14:00,endtime=180',
    'list': 'list'
}

async def extract_host_params(message):
    """
    Extract host command parameters
    """
    content = message.content.replace('host ', '')
    parts = content.split(',')

    name = ''
    player = 0
    date = ''
    endtime = 0.0
    timezone = None

    for part in parts:
        if '=' in part:
            param_name, param_value = part.split('=')
            param_value = param_value.strip()

            if param_name == GameEvent.NAME:
                name = param_value
            elif param_name == GameEvent.PLAYER:
                try:
                    player = int(param_value)
                except:
                    await message.channel.send("Invalid integer value for player")
                    return
            elif param_name == GameEvent.DATE:
                date = param_value
            elif param_name == GameEvent.ENDTIME:
                try:
                    endtime = float(param_value)
                except:
                    await message.channel.send("Invalid float value for endtime")
                    return
            elif param_name == GameEvent.TIMEZONE:
                timezone = param_value
    
    if not name or player <= 0 or not date or endtime <= 0.0:
        await message.channel.send('Please provide name, player (as a positive integer), date, and endtime (as a float integer) after the `host` command.')
        return
    
    creator = {
        GameEvent.CREATOR_ID: message.author.id,
        GameEvent.CREATOR_DISPLAY_NAME: message.author.display_name
    }
    
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
        except Exception:
            await message.channel.send("Please refer to the website for all available timezone: https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568")
            return
    
    return name, player, date, endtime, creator, timezone

async def help(message):
    """
    Show all the available commands.
    """
    help_message = ">>> ## Here are the available commands\n"
    for command, description in command_descriptions.items():
        help_message += f"{command}: {description}\n"
        help_message += f"{command_usages[command]}\n"
        help_message += f"```\n"
        help_message += f"{command_examples[command]}"
        help_message += f"```\n"
    await message.channel.send(help_message)

async def host(message):
    """
    Schedule a game event.
    """
    try:
        name, player, date, endtime, creator, timezone = await extract_host_params(message)
    except:
        return
    
    now = datetime_helper.get_time(specific_timezone = timezone)
    game_event = GameEvent(
        name = name,
        player = player,
        date = date,
        endtime = endtime,
        creator = creator,
        createtime = now,
        timezone = timezone
    )
    
    response_message_content = 'Received'
    response_message = await message.channel.send(response_message_content)
    await response_message.add_reaction('⚔️')
    key = response_message.id

    game_events = await json_helper.load()
    game_events[key] = game_event.to_dict()
    await json_helper.save(game_events)

    updated_message_content = await game_event.get_messages()
    await response_message.edit(content=updated_message_content)
#    try:
#        updated_message_content = await game_event.get_messages()
#        await response_message.edit(content=updated_message_content)
#    except Exception as e:
#        await message.channel.send("An error occurred while updating the game session details. Please try again later.")

async def list(message):
    """
    List existing scheduled game events.
    """
    content = message.content.replace('host ', '')
    parts = content.split(' ')

    filter_available = False
    filter_creator = False

    for part in parts:
        if '-a' in part:
            filter_available = True
        elif '-c' in part:
            filter_creator = True

    game_events_list = []
    game_events = await json_helper.load()

    for _, value in game_events.items():
        timezone = pytz.timezone(value[GameEvent.TIMEZONE])
        now = datetime_helper.get_time(specific_timezone = timezone)

    if game_events_list:
        await message.channel.send('Scheduled game events:')
        await message.channel.send('\n'.join(game_events_list))
    else:
        await message.channel.send('No scheduled game events found.')
