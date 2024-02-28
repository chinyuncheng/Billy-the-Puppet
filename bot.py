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
from discord import app_commands
from discord.ext import commands

import core.commands as core_commands
import settings
from utils import discord_helper

logger = settings.logging.getLogger("bot")

bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())

@bot.event
async def on_ready():
    logger.info(f"{bot.user} (ID: {bot.user.id})".format(bot))
    await bot.tree.sync(guild=settings.GUILD_ID)

@bot.event
async def on_raw_reaction_add(payload):
    await discord_helper.on_raw_reaction_add(payload, bot)

@bot.event
async def on_raw_reaction_remove(payload):
    await discord_helper.on_raw_reaction_remove(payload, bot)

@bot.tree.command(
    name="help",
    description="Show all the available commands.",
    guild=settings.GUILD_ID,
)
@app_commands.describe(param_1="This is required.")
@app_commands.describe(param_2="This is not required.")
async def help_command(
    interaction: discord.Interaction,
    param_1: str,
    param_2: str = "Optional"
    ):
    await core_commands.help(interaction)

if settings.DISCORD_BOT_TOKEN  is None:
    logger.error("Not found DISCORD_BOT_TOKEN in environment variable.")
    exit(1)

bot.run(settings.DISCORD_BOT_TOKEN)
