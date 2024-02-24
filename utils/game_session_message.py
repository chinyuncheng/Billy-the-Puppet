import datetime
import game_session_keys
import pytz
from utils.datetime_helper import get_time, get_timezone_offsets_in_gmt

async def update_message(session_data):
    """
    Update the game session message.
    """
    timezone = pytz.timezone(session_data[game_session_keys.TIMEZONE])
    sign, offset_hours = get_timezone_offsets_in_gmt(timezone)

    date = datetime.datetime.fromisoformat(session_data[game_session_keys.DATE]).strftime('%-m/%d %H:%M')
    date += f" GMT{sign}{offset_hours}"

    endtime = session_data[game_session_keys.ENDTIME]
    created_at = datetime.datetime.fromisoformat(session_data[game_session_keys.CREATED_AT])
    
    now = get_time(specific_timezone=timezone)
    
    recruitment_end_time = created_at + datetime.timedelta(hours=endtime)

    remaining_time_str = 'Recruitment ends'
    if (recruitment_end_time > now):
        remaining_time = recruitment_end_time - now
        days = remaining_time.days
        hours, remainder = divmod(remaining_time.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        
        remaining_time_str += f" in "
        if days > 0:
            remaining_time_str += f"{days} days "
        if hours > 0:
            remaining_time_str += f"{hours} hrs "
        if minutes > 0:
            remaining_time_str += f"{minutes} mins"
        remaining_time_str += f"\nfrom when this message was sent"

    num_participants = len(session_data[game_session_keys.PARTICIPANTS])
    slots = session_data[game_session_keys.PLAYER] - num_participants

    message = (
        f">>> ## {session_data[game_session_keys.NAME]}  {date} [{slots} Slots]\n"
        f"{remaining_time_str}\n"
        f"```\n"
    )

    if num_participants > 0:
        participants_list = "\n".join([f"{i+1:2}. {value}" for i, (_, value) in enumerate(session_data[game_session_keys.PARTICIPANTS].items())])
        message += participants_list
    else:
        message += "No participants yet."
    message += f"```\n"

    author = ''
    for _, value in session_data[game_session_keys.CREATED_BY].items():
        author = value

    message += f"Hosted by {author} | React to the message to join"

    return message
