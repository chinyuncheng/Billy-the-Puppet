import discord
import game_event.keys
import game_event.message
import utils.json_helper

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
    
    game_events = utils.json_helper.load()

    for _, value in game_events.items():
        if payload.message_id == value[game_event.keys.MESSAGE_ID]:
            participants_dict = value[game_event.keys.PARTICIPANTS]
            
            if payload.user_id in participants_dict:
                break
            
            user = await client.fetch_user(payload.user_id)
            participants_dict[f'{payload.user_id}'] = user.display_name
            value[game_event.keys.PARTICIPANTS] = participants_dict
            utils.json_helper.save(game_events)

            updated_message_content = await game_event.message.update_message(value)
            await message.edit(content=updated_message_content)
            break

async def on_raw_reaction_remove(payload, client):
    """
    The on_raw_reaction_remove extension version, add function signature `client`
    """
    message = await get_message(client, payload.channel_id, payload.message_id)
    if message is None:
        return
    
    game_events = utils.json_helper.load()

    for _, value in game_events.items():
        if payload.message_id == value[game_event.keys.MESSAGE_ID]:
            participants_dict = value[game_event.keys.PARTICIPANTS]

            key = f'{payload.user_id}'
            if key not in participants_dict:
                break

            del participants_dict[key]
            value[game_event.keys.PARTICIPANTS] = participants_dict
            utils.json_helper.save(game_events)

            updated_message_content = await game_event.message.update_message(value)
            await message.edit(content=updated_message_content)
            break
