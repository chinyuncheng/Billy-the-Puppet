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

from discord import app_commands
from discord.ext import commands
import asyncio
import discord
import pytz
import traceback
import typing

from core.guild_infos import GuildInfo
from languages import Language
from utils import discord_helper, game_event_helper, json_helper, os_helper
import core.commands as core_commands
import settings

logger = settings.logging.getLogger("bot")

bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    logger.error(f"Error in command '{ctx.command}': {error}")
    traceback.print_exc()

@bot.event
async def on_guild_join(guild):
    if settings.ALLOW_ADD_NEW_GUILD:
        logger.info(f'Joined new guild: {guild.name} (ID: {guild.id})')

        path = os_helper.create_folder(f"{GuildInfo.ROOT_FOLDER}", f"{guild.id}")
        guildinfo = GuildInfo(guild.id, path, settings.DEFAULT_LANGUAGE, pytz.timezone(settings.DEFAULT_TIMEZONE))
        await json_helper.save(guildinfo.to_dict(), guildinfo.get_json_path())
        await initialize_guild(guild)

@bot.event
async def on_raw_reaction_add(payload):
    await discord_helper.on_raw_reaction_add(payload, bot)

@bot.event
async def on_raw_reaction_remove(payload):
    await discord_helper.on_raw_reaction_remove(payload, bot)

@bot.event
async def on_ready():
    logger.info(f"{bot.user} (ID: {bot.user.id})".format(bot))

    for guild in bot.guilds:
        await initialize_guild(guild)

    await schedule_task()

async def initialize_guild(guild: discord.Guild):
    guild_info_dict = await json_helper.load(f"{GuildInfo.ROOT_FOLDER}{guild.id}/{GuildInfo.GUILD_INFO_JSON}")

    if guild_info_dict:
        logger.info(f"Initializing for guild: {guild.name} (ID: {guild.id})")
        guildinfo = GuildInfo.from_dict(guild_info_dict)

        await unregister_commands(guild)

        async def autocompletion_language(
            interaction: discord.Interaction,
            current: str
        ) -> typing.List[app_commands.Choice[str]]:
            data = []
            for language_choice in Language.get_languages():
                if current.lower() in language_choice.lower():
                    data.append(app_commands.Choice(name=language_choice, value=language_choice))
            return data

        @bot.tree.command(
            name=core_commands.COMMAND_HELP,
            description=Language.get_translation(Language.COMMAND_HELP_DESCRIPTION, guildinfo.language),
            guild=guild,
        )
        async def command_help(interaction: discord.Interaction):
            await core_commands.help(interaction, guildinfo)

        @bot.tree.command(
            name=core_commands.COMMAND_HOST,
            description=Language.get_translation(Language.COMMAND_HOST_DESCRIPTION, guildinfo.language),
            guild=guild
        )
        @app_commands.describe(name=Language.get_translation(Language.COMMAND_HOST_PARAM_NAME, guildinfo.language))
        @app_commands.describe(player=Language.get_translation(Language.COMMAND_HOST_PARAM_PLAYER, guildinfo.language))
        @app_commands.describe(date=Language.get_translation(Language.COMMAND_HOST_PARAM_DATE, guildinfo.language))
        @app_commands.describe(endtime=Language.get_translation(Language.COMMAND_HOST_PARAM_ENDTIME, guildinfo.language))
        @app_commands.describe(timezone=Language.get_translation(Language.COMMAND_HOST_PARAM_TIMEZONE, guildinfo.language))
        async def command_host(
            interaction: discord.Interaction,
            name: str,
            player: int,
            date: str,
            endtime: float,
            timezone: str = None
        ):
            await core_commands.host(interaction, name, player, date, endtime, timezone, guildinfo)

        @bot.tree.command(
            name=core_commands.COMMAND_LIST,
            description=Language.get_translation(Language.COMMAND_LIST_DESCRIPTION, guildinfo.language),
            guild=guild
        )
        @app_commands.describe(available=Language.get_translation(Language.COMMAND_LIST_PARAM_AVAILABLE, guildinfo.language))
        @app_commands.describe(creator=Language.get_translation(Language.COMMAND_LIST_PARAM_CREATOR, guildinfo.language))
        async def command_list(
            interaction: discord.Integration,
            available: bool = False,
            creator: bool = False,
        ):
            await core_commands.list(interaction, available, creator, guildinfo)

        @bot.tree.command(
            name=core_commands.COMMAND_MODIFY,
            description=Language.get_translation(Language.COMMAND_MODIFY_DESCRIPTION, guildinfo.language),
            guild=guild
        )
        @app_commands.autocomplete(language=autocompletion_language)
        @app_commands.describe(language=Language.get_translation(Language.COMMAND_MODIFY_PARAM_LANGUAGE, guildinfo.language))
        @app_commands.describe(timezone=Language.get_translation(Language.COMMAND_MODIFY_PARAM_TIMEZONE, guildinfo.language))
        async def command_modify(
            interaction: discord.Integration,
            language: str = None,
            timezone: str = None
        ):
            re_initialize = await core_commands.modify(interaction, language, timezone, guildinfo)
            if re_initialize:
                message = Language.get_translation(Language.COMMAND_MODIFY_PROCESS, guildinfo.language)
                await interaction.response.send_message(message, ephemeral=True, delete_after=7)
                await initialize_guild(guild)

        await bot.tree.sync(guild=guild)

async def schedule_task():
    hours_in_seconds = 3600
    while True:
        await scheduled_task()
        await asyncio.sleep(settings.GAME_EVENTS_DELETION_PERIOD_IN_HOURS * hours_in_seconds)

async def scheduled_task():
    await game_event_helper.delete_recruitment_end_game_events(bot)

async def unregister_commands(guild: discord.Guild):
    if guild:
        bot.remove_command("help")
        for command_name in core_commands.get_commands():
            try:
                bot.tree.remove_command(command_name, guild=guild)
            except Exception as e:
                logger.error(f"Failed to unregister command '{command_name}' from guild ID {guild.id}: {e}")
    else:
        logger.warning(f"Guild not found.")

if __name__ == "__main__":
    if settings.DISCORD_BOT_TOKEN is None:
        logger.error("DISCORD_BOT_TOKEN not found in environment variable.")
        exit(1)
    try:
        bot.run(settings.DISCORD_BOT_TOKEN)
    except Exception as e:
        logger.error(f"An error occurred while running the bot: {e}")
        traceback.print_exc()
 