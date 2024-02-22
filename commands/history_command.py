from . import command_descriptions
from datetime import datetime

async def history_command(message):
    parts = message.content.split(maxsplit=2)
    if len(parts) < 3:
        await message.channel.send('Please provide start_date and end_date after the `history` command.')
        return
    start_date, end_date = parts[1:]

    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        await message.channel.send('Invalid date format. Please use the format YYYY-MM-DD.')
        return

    session_list = [f'{name} - {session["time"]}' for name, session in command_descriptions.items() if start_date <= datetime.strptime(session["scheduled_time"], '%Y-%m-%d %H:%M:%S') <= end_date]

    if session_list:
        await message.channel.send('Game sessions within the specified date range:')
        await message.channel.send('\n'.join(session_list))
    else:
        await message.channel.send('No game sessions found within the specified date range.')
