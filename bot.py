import os
import discord
from dotenv import load_dotenv
from commands import help_command, host_command, list_command

load_dotenv()

TOKEN = os.getenv('DISCORD_BOT_TOKEN')

if TOKEN is None:
    print("Error: Bot token not found in environment variable DISCORD_BOT_TOKEN.")
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

    if content.startswith('help'):
        await help_command.help_command(message)

    elif content.startswith('host'):
        await host_command.host_command(message, client)

    elif content.startswith('list'):
        await list_command.list_command(message)

@client.event
async def on_reaction_add(reaction, user):
    if user == client.user:
        return
    await reaction.message.channel.send('User add reaction')

client.run(TOKEN)
