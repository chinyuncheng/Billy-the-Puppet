import os
import discord
from dotenv import load_dotenv
from commands import help_command, history_command, host_command, list_command

load_dotenv()

TOKEN = os.getenv('DISCORD_BOT_TOKEN')

if TOKEN is None:
    print("Error: Bot token not found in environment variable DISCORD_BOT_TOKEN.")
    exit(1)

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!help'):
        await help_command.help_command(message)

    elif message.content.startswith('!history'):
        await history_command.history_command(message)

    elif message.content.startswith('!host'):
        await host_command.host_command(message)

    elif message.content.startswith('!list'):
        await list_command.list_command(message)

client.run(TOKEN)
