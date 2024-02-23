import discord
from utils.json_helper import save_game_sessions, load_game_sessions
from utils.game_session_message import update_message

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
    The on_raw_reaction_add extension version, add function signature `client`
    """
    message = await get_message(client, payload.channel_id, payload.message_id)
    if message is None:
        return

    if payload.member.bot:
        return
    
    game_sessions = load_game_sessions()

    for _, value in game_sessions.items():
        if payload.message_id == value['message_id']:
            participants_dict = value['participants']
            
            if payload.user_id in participants_dict:
                break
            
            user = await client.fetch_user(payload.user_id)
            participants_dict[f'{payload.user_id}'] = user.display_name
            value['participants'] = participants_dict
            save_game_sessions(game_sessions)

            updated_message_content = await update_message(value)
            await message.edit(content=updated_message_content)
            break

async def on_raw_reaction_remove(payload, client):
    """
    The on_raw_reaction_remove extension version, add function signature `client`
    """
    message = await get_message(client, payload.channel_id, payload.message_id)
    if message is None:
        return
    
    game_sessions = load_game_sessions()

    for _, value in game_sessions.items():
        if payload.message_id == value['message_id']:
            participants_dict = value['participants']

            key = f'{payload.user_id}'
            if key not in participants_dict:
                break

            del participants_dict[key]
            value['participants'] = participants_dict
            save_game_sessions(game_sessions)

            updated_message_content = await update_message(value)
            await message.edit(content=updated_message_content)
            break
