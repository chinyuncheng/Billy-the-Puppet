import os
import discord
from dotenv import load_dotenv
from commands import command_help, command_host, command_list

load_dotenv()

TOKEN = os.getenv('DISCORD_BOT_TOKEN')

if TOKEN is None:
    print("Error: Bot Token not found in environment variable DISCORD_BOT_TOKEN.")
    exit(1)

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    content = message.content.lower().strip()

    if isinstance(message.channel, discord.DMChannel):
        if content.startswith('help'):
            await command_help.help_command(message)
        return
    
    else:
        if content.startswith('host'):
            await command_host.host_command(message, client)

        elif content.startswith('list'):
            await command_list.list_command(message)

client.run(TOKEN)
