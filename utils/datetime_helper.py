import config
import datetime
import pytz
import time

def get_time(date=None, specific_timezone=pytz.timezone(config.TIMEZONE)):
    """
    Convert time to a specific timezone if necessary.
    """
    if date is None:
        date = datetime.datetime.now()

    current_timezone_name = time.tzname[time.localtime().tm_isdst]
    current_timezone = pytz.timezone(current_timezone_name)

    if current_timezone != specific_timezone:
        date = current_timezone.localize(date, is_dst=None).astimezone(specific_timezone)

    return date

def get_timezone_offsets_in_gmt(timezone=pytz.timezone(config.TIMEZONE)):
    """
    Get UTC offset in GMT format
    """
    utc_time = datetime.datetime.utcnow()
    offset = timezone.utcoffset(utc_time)
    offset_hours = int(offset.total_seconds() // 3600)
    sign = '+' if offset_hours >= 0 else '-'
    offset_hours = abs(offset_hours)

    return sign, offset_hours
