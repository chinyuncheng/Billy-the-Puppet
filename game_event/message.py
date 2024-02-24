import game_event.keys
import game_event.message_helper

async def update_message(game_event_item):
    """
    Update the game event message.
    """
    title_msg = game_event.message_helper.get_title_message(game_event_item)
    slots_msg = game_event_item[game_event.keys.PLAYER] - len(game_event_item[game_event.keys.PARTICIPANTS])
    remaining_time_msg = game_event.message_helper.get_remaining_time_message(game_event_item)
    participants_msg = game_event.message_helper.get_participants_message(game_event_item)
    author_msg = game_event.message_helper.get_author_message(game_event_item)

    message = (
        f">>> ## {title_msg} [{slots_msg} Slots]\n"
        f"{remaining_time_msg}\n"
        f"```\n"
        f"{participants_msg}"
        f"```\n"
        f"{author_msg}"
    )

    return message
