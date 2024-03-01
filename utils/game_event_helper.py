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

from discord.ext import commands

from core.game_events import GameEvent
from utils import discord_helper, json_helper
import settings

logger = settings.logging.getLogger("bot")

async def delete_recruitment_end_game_events(bot: commands.Bot):
    """
    Update the message and delete the game event from the JSON file if its recruitment ends
    """
    game_events = await json_helper.load()
    list_to_delete = []

    for key, value in game_events.items():
        game_event = GameEvent.from_dict(value)

        if game_event.is_recruitment_end()[0]:
            list_to_delete.append(key)
            message = await discord_helper.get_message(bot, settings.CHANNEL_ID, int(key))

            if message:
                game_event = GameEvent.from_dict(value)
                updated_message_content = game_event.get_messages()
                await message.edit(content = updated_message_content)

    for item in list_to_delete:
        del game_events[item]
    await json_helper.save(game_events)
