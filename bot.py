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

import discord
import settings
from core import commands
from utils import discord_helper

logger = settings.logging.getLogger("bot")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    logger.info(f"{client.user} (ID: {client.user.id})".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    content = message.content.lower().strip()

    if isinstance(message.channel, discord.DMChannel):
        if content.startswith('help'):
            await commands.help(message)
        return
    
    else:
        if content.startswith('host'):
            await commands.host(message)

        elif content.startswith('list'):
            await commands.list(message)

@client.event
async def on_raw_reaction_add(payload):
    await discord_helper.on_raw_reaction_add(payload, client)

@client.event
async def on_raw_reaction_remove(payload):
    await discord_helper.on_raw_reaction_remove(payload, client)

if settings.DISCORD_BOT_TOKEN  is None:
    logger.error("Not found DISCORD_BOT_TOKEN in environment variable.")
    exit(1)

client.run(settings.DISCORD_BOT_TOKEN)
