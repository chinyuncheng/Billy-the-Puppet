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

import asyncio
import discord
import traceback
from discord import app_commands
from discord.ext import commands

import core.commands as core_commands
import settings
from utils import discord_helper, game_event_helper

logger = settings.logging.getLogger("bot")

bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    logger.error(f"Error in command '{ctx.command}': {error}")
    traceback.print_exc()

@bot.event
async def on_ready():
    logger.info(f"{bot.user} (ID: {bot.user.id})".format(bot))
    await bot.tree.sync(guild=settings.GUILD_ID)
    await schedule_task()

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
async def command_help(interaction: discord.Interaction):
    await core_commands.help(interaction)

@bot.tree.command(
    name="host",
    description="Schedule a game event.",
    guild=settings.GUILD_ID
)
@app_commands.describe(name="The game event name.")
@app_commands.describe(player="The number of players.")
@app_commands.describe(date="The game event date. Please provide in the format \"YYYY-MM-DD HH:MM\".")
@app_commands.describe(endtime="The recruitment period will end in (hours).")
@app_commands.describe(timezone="The timezone of the game event.")
async def command_host(
    interaction: discord.Interaction,
    name: str,
    player: int,
    date: str,
    endtime: float,
    timezone: str = None
):
    await core_commands.host(interaction, name, player, date, endtime, timezone)

@bot.tree.command(
    name="list",
    description="List existing scheduled game events.",
    guild=settings.GUILD_ID
)
@app_commands.describe(available="To filter the game events that are still in recruitment.")
@app_commands.describe(creator="To filter the game events that are created on your own.")
async def command_list(
    interaction: discord.Integration,
    available: bool = False,
    creator: bool = False
):
    await core_commands.list(interaction, available, creator)

async def schedule_task():
    hours_in_seconds = 3600
    while True:
        await scheduled_task()
        await asyncio.sleep(settings.GAME_EVENTS_DELETION_PERIOD_IN_HOURS * hours_in_seconds)

async def scheduled_task():
    await game_event_helper.delete_recruitment_end_game_events(bot)

if __name__ == "__main__":
    if settings.DISCORD_BOT_TOKEN is None:
        logger.error("DISCORD_BOT_TOKEN not found in environment variable.")
        exit(1)
    try:
        bot.run(settings.DISCORD_BOT_TOKEN)
    except Exception as e:
        logger.error(f"An error occurred while running the bot: {e}")
        traceback.print_exc()
