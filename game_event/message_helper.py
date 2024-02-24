import datetime
import game_event.keys
import pytz
import utils.datetime_helper

def get_title_message(game_event_item):
    """
    Get title message from game event
    """
    date_msg = get_date_message(game_event_item)
    return f"{game_event_item[game_event.keys.NAME]}  {date_msg}"

def get_date_message(game_event_item):
    """
    Get date message from game event
    """
    timezone = pytz.timezone(game_event_item[game_event.keys.TIMEZONE])
    sign, offset_hours = utils.datetime_helper.get_timezone_offsets_in_gmt(timezone)

    date_msg = datetime.datetime.fromisoformat(game_event_item[game_event.keys.DATE]).strftime('%-m/%d %H:%M')
    date_msg += f" GMT{sign}{offset_hours}"

    return date_msg

def get_remaining_time_message(game_event_item):
    """
    Get remaining time message from game event
    """
    endtime = game_event_item[game_event.keys.ENDTIME]
    created_at = datetime.datetime.fromisoformat(game_event_item[game_event.keys.CREATED_AT])
    
    timezone = pytz.timezone(game_event_item[game_event.keys.TIMEZONE])
    now = utils.datetime_helper.get_time(specific_timezone=timezone)
    
    recruitment_end_time = created_at + datetime.timedelta(hours=endtime)

    remaining_time_msg = 'Recruitment ends'
    if (recruitment_end_time > now):
        remaining_time = recruitment_end_time - now
        days = remaining_time.days
        hours, remainder = divmod(remaining_time.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        
        remaining_time_msg += f" in "
        if days > 0:
            remaining_time_msg += f"{days} days "
        if hours > 0:
            remaining_time_msg += f"{hours} hrs "
        if minutes > 0:
            remaining_time_msg += f"{minutes} mins"
        remaining_time_msg += f"\nfrom when this message was sent"
    
    return remaining_time_msg

def get_participants_message(game_event_item):
    """
    Get participants message from game event
    """
    participants_msg = ''
    num_participants = len(game_event_item[game_event.keys.PARTICIPANTS])

    if num_participants > 0:
        participants_list = "\n".join([f"{i+1:2}. {value}" for i, (_, value) in enumerate(game_event_item[game_event.keys.PARTICIPANTS].items())])
        participants_msg += participants_list
    else:
        participants_msg = "No participants yet."
    
    return participants_msg

def get_author_message(game_event_item):
    """
    Get author message from game event
    """
    author = ''
    for _, value in game_event_item[game_event.keys.CREATED_BY].items():
        author = value

    return f"Hosted by {author} | React to the message to join"
