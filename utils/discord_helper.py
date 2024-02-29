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

from core.game_events import GameEvent
from utils import json_helper
import discord

async def get_message(client, channel_id, message_id):
    """
    Get message from channel through message id.
    """
    try:
        channel = await client.fetch_channel(channel_id)
        return await channel.fetch_message(message_id)
    except discord.NotFound:
        print(f"Message with ID {message_id} not found.")
        return None

async def on_raw_reaction_add(payload, client):
    """
    The on_raw_reaction_add extension version, add function signature `client`.
    """
    message = await get_message(client, payload.channel_id, payload.message_id)
    if message is None:
        return
    if payload.member.bot:
        return
    if payload.emoji.name != '⚔️':
        return
    
    game_events = await json_helper.load()

    for key, value in game_events.items():
        if str(payload.message_id) == key:
            participants_dict = value[GameEvent.PARTICIPANTS]
            if payload.user_id in participants_dict:
                break
            
            user = await client.fetch_user(payload.user_id)
            participants_dict[f'{payload.user_id}'] = user.display_name
            value[GameEvent.PARTICIPANTS] = participants_dict
            await json_helper.save(game_events)

            game_event = GameEvent.from_dict(value)
            updated_message_content = game_event.get_messages()
            await message.edit(content = updated_message_content)
            break

async def on_raw_reaction_remove(payload, client):
    """
    The on_raw_reaction_remove extension version, add function signature `client`.
    """
    message = await get_message(client, payload.channel_id, payload.message_id)
    if message is None:
        return
    if payload.emoji.name != '⚔️':
        return
    
    game_events = await json_helper.load()

    for key, value in game_events.items():
        if str(payload.message_id) == key:
            participants_dict = value[GameEvent.PARTICIPANTS]

            key = f'{payload.user_id}'
            if key not in participants_dict:
                break

            del participants_dict[key]
            value[GameEvent.PARTICIPANTS] = participants_dict
            await json_helper.save(game_events)

            game_event = GameEvent.from_dict(value)
            updated_message_content = game_event.get_messages()
            await message.edit(content = updated_message_content)
            break
