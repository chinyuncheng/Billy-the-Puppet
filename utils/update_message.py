import datetime

async def update_message(session_data):
    """
    Update the game session message.
    """
    scheduled_time = datetime.datetime.strptime(session_data['scheduled_time'], '%Y-%m-%dT%H:%M:%S%z').strftime('%Y-%m-%d %H:%M (GMT+8)')
    recruitment_end_time = datetime.datetime.strptime(session_data['recruitment_end_time'], '%Y-%m-%dT%H:%M:%S%z').strftime('%Y-%m-%d %H:%M (GMT+8)')

    num_participants = len(session_data['participants'])
    slots = session_data['players'] - num_participants

    message = (
        f"# {session_data['name']}\n"
        f"Scheduled Time: {scheduled_time}\n"
        f"Recruitment Ends: {recruitment_end_time}\n\n"
        f"Available Slots: {slots}\n"
        f"Participants:\n"
    )

    if num_participants > 0:
        message += "\n".join([f"{i}. {participant}" for i, participant in enumerate(session_data['participants'], start=1)])
    else:
        message += "No participants yet."

    message += f"\n\nHosted by {session_data['created_by']} | React to the message to join"

    return message
