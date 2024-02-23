from . import command_descriptions, command_usages, command_examples

async def help_command(message):
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
