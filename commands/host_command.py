from . import command_descriptions
from datetime import datetime

async def host_command(message):
    parts = message.content.split(maxsplit=4)
    if len(parts) < 3:
        await message.channel.send('Please provide event_name, players, and time after the `!host` command.')
        return
    event_name, players, time = parts[1:4]

    description = parts[4] if len(parts) > 4 else None

    command_descriptions.command_descriptions[event_name] = {
        'players': players,
        'time': time,
        'description': description,
        'scheduled_time': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    await message.channel.send(f'Game session "{event_name}" scheduled for {time}! Who\'s joining?')
