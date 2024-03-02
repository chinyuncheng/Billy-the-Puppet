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
import os

from core.game_events import GameEvent
from core.guild_infos import GuildInfo
from utils import discord_helper, json_helper, os_helper
import settings

logger = settings.logging.getLogger("bot")

async def delete_recruitment_end_game_events(bot: commands.Bot):
    """
    Update the message and delete the game event from the JSON file if its recruitment ends
    """
    json_file_list = os_helper.get_files(GuildInfo.ROOT_FOLDER, ".json")

    for json_file in json_file_list:
        if json_file.find(GuildInfo.GUILD_INFO_JSON) != -1:
            continue

        parent_folder_path = os.path.dirname(json_file)
        guildinfo_json = await json_helper.load(f"{parent_folder_path}/{GuildInfo.GUILD_INFO_JSON}")
        guildinfo = GuildInfo.from_dict(guildinfo_json)

        filename_with_extension = os.path.basename(json_file)
        filename_without_extension = os.path.splitext(filename_with_extension)[0]

        game_events = await json_helper.load(json_file)
        list_to_delete = []

        for key, value in game_events.items():
            game_event = GameEvent.from_dict(value)

            if game_event.is_recruitment_end()[0]:
                list_to_delete.append(key)
                message = await discord_helper.get_message(bot, int(filename_without_extension), int(key))

                if message:
                    game_event = GameEvent.from_dict(value)
                    updated_message_content = game_event.get_messages(guildinfo.language)
                    await message.edit(content = updated_message_content)

        for item in list_to_delete:
            del game_events[item]
        await json_helper.save(game_events, json_file)
