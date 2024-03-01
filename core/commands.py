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

import datetime
import discord
import pytz

import settings
from core.game_events import GameEvent
from languages import Language
from utils import json_helper

command_descriptions = {
    "/host": Language.get_translation(Language.COMMAND_HOST_DESCRIPTION, settings.LANGUAGE),
    "/list": Language.get_translation(Language.COMMAND_LIST_DESCRIPTION, settings.LANGUAGE)
}

async def help(interaction: discord.Interaction):
    """
    Show all the available commands.
    """
    help_message = f">>> ## {Language.get_translation(Language.COMMAND_HELP_RESULT, settings.LANGUAGE)}\n"
    for command, description in command_descriptions.items():
        help_message += f"`{command}` {description}\n"
    await interaction.response.send_message(f"{help_message}", ephemeral=True)

async def host(
    interaction: discord.Interaction,
    name: str,
    player: int,
    date: datetime.datetime,
    endtime: float,
    timezone: str
):
    """
    Schedule a game event.
    """
    if player <= 0:
        message = Language.get_translation(Language.COMMAND_HOST_PARAM_PLAYER_HINT, settings.LANGUAGE)
        await interaction.response.send_message(message, ephemeral=True)
        return

    if endtime <= 0.0:
        message = Language.get_translation(Language.COMMAND_HOST_PARAM_ENDTIME_HINT, settings.LANGUAGE)
        await interaction.response.send_message(message, ephemeral=True)
        return

    try:
        date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M')
    except ValueError:
        message = Language.get_translation(Language.COMMAND_HOST_PARAM_DATE_HINT, settings.LANGUAGE)
        await interaction.response.send_message(message, ephemeral=True)
        return

    if timezone is None:
        timezone = pytz.timezone(settings.TIMEZONE)
    else:
        try:
            timezone = pytz.timezone(timezone)
        except Exception:
            message = Language.get_translation(Language.COMMAND_HOST_PARAM_TIMEZONE_HINT, settings.LANGUAGE)
            await interaction.response.send_message(message, ephemeral=True)
            return

    user = interaction.user
    creator = {
        GameEvent.CREATOR_ID: user.id,
        GameEvent.CREATOR_DISPLAY_NAME: user.display_name
    }

    now = datetime.datetime.now(tz=timezone)
    game_event = GameEvent(
        name = name,
        player = player,
        date = date,
        endtime = endtime,
        creator = creator,
        createtime = now,
        timezone = timezone
    )

    response_message_content = Language.get_translation(Language.COMMAND_HOST_RECEIVE, settings.LANGUAGE)
    await interaction.response.send_message(response_message_content, delete_after=3)

    response_message_content = Language.get_translation(Language.COMMAND_HOST_PROCESS, settings.LANGUAGE)
    response_message = await interaction.channel.send(response_message_content)
    await response_message.add_reaction('⚔️')
    key = response_message.id

    game_events = await json_helper.load(settings.GAME_EVENTS_FILE_PATH)
    game_events[key] = game_event.to_dict()
    await json_helper.save(game_events, settings.GAME_EVENTS_FILE_PATH)

    try:
        updated_message_content = game_event.get_messages()
        await response_message.edit(content=updated_message_content)
    except Exception as e:
        message = Language.get_translation(Language.COMMAND_HOST_UPDATE_ERROR, settings.LANGUAGE)
        await message.channel.send(message)

async def list(
    interaction: discord.Interaction,
    available: bool,
    creator: bool
):
    """
    List existing scheduled game events.
    """
    game_events_list = []
    game_events = await json_helper.load(settings.GAME_EVENTS_FILE_PATH)

    for _, value in game_events.items():
        game_event = GameEvent.from_dict(value)

        if (game_event.is_expired()):
            game_event = None
        if (game_event is not None and available and (game_event.is_recruitment_end()[0] or game_event.is_recruitment_full())):
            game_event = None
        if (game_event is not None and creator and interaction.user.id != game_event.creator[GameEvent.CREATOR_ID]):
            game_event = None

        if (game_event is not None):
            game_events_list.append(game_event)

    if game_events_list:
        list_message = f">>> ## {Language.get_translation(Language.COMMAND_LIST_RESULT, settings.LANGUAGE)}\n"
        for item in game_events_list:
            list_message += f"```{item._get_messages_title()}```"
        await interaction.response.send_message(f"{list_message}", ephemeral=True)
    else:
        list_message = f"{Language.get_translation(Language.COMMAND_LIST_RESULT_NOT_FOUND, settings.LANGUAGE)}"
        await interaction.response.send_message(list_message, ephemeral=True)
