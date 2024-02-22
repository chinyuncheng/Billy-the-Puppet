from . import command_descriptions
from datetime import datetime

async def list_command(message):
    attendable = False
    if '-a' in message.content.split():
        attendable = True

    current_time = datetime.utcnow()
    if attendable:
        session_list = [f'{name} - {session["time"]}' for name, session in command_descriptions.command_descriptions.items() if datetime.strptime(session["scheduled_time"], '%Y-%m-%d %H:%M:%S') > current_time]
    else:
        session_list = [f'{name} - {session["time"]}' for name, session in command_descriptions.command_descriptions.items()]
    
    if session_list:
        await message.channel.send('Scheduled game sessions:')
        await message.channel.send('\n'.join(session_list))
    else:
        await message.channel.send('No scheduled game sessions found.')
