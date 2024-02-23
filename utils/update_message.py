import datetime

async def update_message(session_data):
    """
    Update the game session message.
    """
    scheduled_time = datetime.datetime.strptime(session_data['scheduled_time'], '%Y-%m-%dT%H:%M:%S%z').strftime('%-m/%d %H:%M GMT+8')
    recruitment_end_time = datetime.datetime.strptime(session_data['recruitment_end_time'], '%Y-%m-%dT%H:%M:%S%z')
    
    remaining_time = recruitment_end_time - datetime.datetime.now(recruitment_end_time.tzinfo)
    days = remaining_time.days
    hours, remainder = divmod(remaining_time.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    remaining_time_str = f"Recruitment Ends in "
    if days > 0:
        remaining_time_str += f"{days} days "
    if hours > 0:
        remaining_time_str += f"{hours} hrs "
    if minutes > 0:
        remaining_time_str += f"{minutes} mins"

    num_participants = len(session_data['participants'])
    slots = session_data['players'] - num_participants

    message = (
        f">>> ## {session_data['name']} {scheduled_time} [{slots} Slots]\n"
        f"{remaining_time_str}\n"
        f"```\n"
    )

    if num_participants > 0:
        participants_list = "\n".join([f"{i+1:2}. {participant}" for i, participant in enumerate(session_data['participants'])])
        message += participants_list
    else:
        message += "No participants yet."
    message += f"```\n"
    message += f"Hosted by {session_data['created_by']} | React to the message to join"

    return message
