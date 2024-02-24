import game_session_keys
from utils.game_session_message_helper import get_title_message, get_remaining_time_message, get_participants_message, get_author_message

async def update_message(game_session):
    """
    Update the game session message.
    """
    title_msg = get_title_message(game_session)
    remaining_time_msg = get_remaining_time_message(game_session)
    slots_msg = game_session[game_session_keys.PLAYER] - len(game_session[game_session_keys.PARTICIPANTS])
    participants_msg = get_participants_message(game_session)
    author_msg = get_author_message(game_session)

    message = (
        f">>> ## {title_msg} [{slots_msg} Slots]\n"
        f"{remaining_time_msg}\n"
        f"```\n"
    )
    message += participants_msg
    message += f"```\n"
    message += author_msg

    return message
