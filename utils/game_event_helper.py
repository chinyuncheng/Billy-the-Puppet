from discord.ext import commands

from core.game_events import GameEvent
from utils import discord_helper, json_helper
import settings

logger = settings.logging.getLogger("bot")

async def delete_recruitment_end_game_events(bot: commands.Bot):
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
