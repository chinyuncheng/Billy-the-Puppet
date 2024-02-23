import discord

async def get_message(channel, message_id):
    try:
        return await channel.fetch_message(message_id)
    except discord.NotFound:
        print(f"Message with ID {message_id} not found.")
        return None