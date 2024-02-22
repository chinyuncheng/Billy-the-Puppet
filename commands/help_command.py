from . import command_descriptions

async def help_command(message):
    help_message = "Here are the available commands:\n"
    for command, description in command_descriptions.command_descriptions.items():
        help_message += f"{command}: {description}\n"
    await message.channel.send(help_message)