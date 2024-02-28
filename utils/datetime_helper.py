"""
MIT License

Copyright (c) 2024-present chinyuncheng

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import datetime
import pytz
import settings
import time

def get_time(date = None, specific_timezone=pytz.timezone(settings.TIMEZONE)):
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

def get_timezone_offsets_in_gmt(timezone=pytz.timezone(settings.TIMEZONE)):
    """
    Get UTC offset in GMT format.
    """
    utc_time = datetime.datetime.utcnow()
    offset = timezone.utcoffset(utc_time)
    offset_hours = int(offset.total_seconds() // 3600)
    sign = '+' if offset_hours >= 0 else '-'
    offset_hours = abs(offset_hours)

    return sign, offset_hours
