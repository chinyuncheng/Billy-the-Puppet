import discord
import os
from commands import help_command, host_command, list_command
from dotenv import load_dotenv
from utils import reaction_helper

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
            await help_command.help_command(message)
        return
    
    else:
        if content.startswith('host'):
            await host_command.host_command(message)

        elif content.startswith('list'):
            await list_command.list_command(message)

@client.event
async def on_raw_reaction_add(payload):
    await reaction_helper.on_raw_reaction_add(payload, client)

@client.event
async def on_raw_reaction_remove(payload):
    await reaction_helper.on_raw_reaction_remove(payload, client)

client.run(TOKEN)
