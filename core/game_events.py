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
from typing import Union
import utils.datetime_helper

class GameEvent:
    """
    The game event class for saving details.
    """
    NAME = 'name'
    PLAYER = 'player'
    DATE = 'date'
    ENDTIME = 'endtime'
    CREATOR = 'creator'
    CREATOR_ID = 'id'
    CREATOR_DISPLAY_NAME = 'display_name'
    CREATETIME = 'createtime'
    TIMEZONE = 'timezone'
    PARTICIPANTS = 'participants'

    def __init__(self, name: str, player: int, date: datetime.datetime, endtime: float,
                 creator: dict, createtime: datetime.datetime, timezone: Union[pytz.tzinfo.StaticTzInfo, pytz.tzinfo.DstTzInfo], participants: dict = {}):
        self._name = name
        self._player = player
        self._date = date
        self._endtime = endtime
        self._creator = creator
        self._createtime = createtime
        self._timezone = timezone
        self._participants = participants

    @property
    def name(self) -> Union[str]:
        return self._name
    
    @name.setter
    def name(self, value: Union[str]):
        if not isinstance(value, (str)):
            raise TypeError("Value must be a string")
        self._name = value
    
    @property
    def player(self) -> Union[int]:
        return self._player
    
    @player.setter
    def player(self, value: Union[int]):
        if not isinstance(value, (int)):
            raise TypeError("Value must be an integer")
        self._player = value
    
    @property
    def date(self) -> Union[datetime.datetime]:
        return self._date
    
    @date.setter
    def date(self, value: Union[datetime.datetime]):
        if not isinstance(value, (datetime.datetime)):
            raise TypeError("Value must be a datetime")
        self._date = value
    
    @property
    def endtime(self) -> Union[float]:
        return self._endtime

    @endtime.setter
    def endtime(self, value: Union[float]):
        if not isinstance(value, (float)):
            raise TypeError("Value must be a float")
        self._endtime = value
    
    @property
    def creator(self) -> Union[dict]:
        return self._creator

    @creator.setter
    def creator(self, value: Union[dict]):
        if not isinstance(value, (dict)):
            raise TypeError("Value must be a dict")
        self._creator = value
    
    @property
    def createtime(self) -> Union[datetime.datetime]:
        return self._createtime

    @createtime.setter
    def createtime(self, value: Union[datetime.datetime]):
        if not isinstance(value, (datetime.datetime)):
            raise TypeError("Value must be a datetime")
        self._createtime = value
    
    @property
    def timezone(self) -> Union[pytz.tzinfo.StaticTzInfo, pytz.tzinfo.DstTzInfo]:
        return self._timezone

    @timezone.setter
    def timezone(self, value: Union[pytz.tzinfo.StaticTzInfo, pytz.tzinfo.DstTzInfo]):
        if not isinstance(value, (pytz.tzinfo.StaticTzInfo, pytz.tzinfo.DstTzInfo)):
            raise TypeError("Value must be a pytz.tzinfo.StaticTzInfo or pytz.tzinfo.DstTzInfo")
        self._timezone = value
    
    @property
    def participants(self) -> Union[dict]:
        return self._participants

    @participants.setter
    def participants(self, value: Union[dict]):
        if not isinstance(value, (dict)):
            raise TypeError("Value must be a dict")
        self._participants = value
    
    @classmethod
    def from_dict(cls, data: dict):
        """
        Get GameEvent instance from dict
        """
        return cls(
            data[cls.NAME],
            data[cls.PLAYER],
            datetime.datetime.fromisoformat(data[cls.DATE]),
            data[cls.ENDTIME],
            data[cls.CREATOR],
            datetime.datetime.fromisoformat(data[cls.CREATETIME]),
            pytz.timezone(data[cls.TIMEZONE]),
            data[cls.PARTICIPANTS]
        )
    
    async def get_messages(self):
        """
        Get messages from current GameEvent instance.
        """
        message_title = GameEvent.get_messages_title(self)
        message_remaining_time = GameEvent.get_messages_remaining_time(self)
        message_participants = GameEvent.get_messages_participants(self)
        message_creator = GameEvent.get_messages_creator(self)

        messages = (
            f">>> ## {message_title}\n"
            f"{message_remaining_time}\n"
            f"```\n"
            f"{message_participants}"
            f"```\n"
            f"{message_creator}"
        )

        return messages
    
    def get_messages_creator(self):
        """
        Get the creator message from current GameEvent instance.
        """
        creator = self.creator[GameEvent.CREATOR_DISPLAY_NAME]
        return f"Hosted by {creator} | React to the message to join"

    def get_messages_date(self):
        """
        Get the date message from current GameEvent instance.
        """
        timezone = self.timezone
        sign, offset_hours = utils.datetime_helper.get_timezone_offsets_in_gmt(timezone)

        message_date = self.date.strftime('%-m/%d %H:%M')
        message_date += f" GMT{sign}{offset_hours}"

        return message_date

    def get_messages_participants(self):
        """
        Get the participants message from current GameEvent instance.
        """
        message_participants = ""
        num_participants = len(self.participants)

        if num_participants > 0:
            participants_list = "\n".join([f"{i+1:2}. {value}" for i, (_, value) in enumerate(self.participants.items())])
            message_participants += participants_list
        else:
            message_participants = "No participants yet."
        
        return message_participants

    def get_messages_remaining_time(self):
        """
        Get the remaining time message from current GameEvent instance.
        """
        is_recruitment, remaining_time = self.is_recruitment()

        message_remaining_time = 'Recruitment ends'
        if (is_recruitment):
            days = remaining_time.days
            hours, remainder = divmod(remaining_time.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            
            message_remaining_time += f" in "
            if days > 0:
                message_remaining_time += f"{days} days "
            if hours > 0:
                message_remaining_time += f"{hours} hrs "
            if minutes > 0:
                message_remaining_time += f"{minutes} mins"
            message_remaining_time += f"\nfrom when this message was sent"
        
        return message_remaining_time

    def get_messages_title(self):
        """
        Get the title message from current GameEvent instance.
        """
        message_date = GameEvent.get_messages_date(self)
        message_slots = self.player - len(self.participants)
        return f"{self.name}  {message_date} [{message_slots} Slots]"

    def is_recruitment(self):
        """
        Check if the game event is still recruitment or not.
        """
        now = utils.datetime_helper.get_time(specific_timezone = self.timezone)
        recruitment_end_time = self.createtime + datetime.timedelta(hours=self.endtime)
        return self.date > now.replace(tzinfo=None) and recruitment_end_time > now, recruitment_end_time - now

    def to_dict(self):
        """
        Convert GameEvent instance to dict.
        """
        return {
            self.NAME: self._name,
            self.PLAYER: self._player,
            self.DATE: self._date.isoformat(),
            self.ENDTIME: self._endtime,
            self.CREATOR: self._creator,
            self.CREATETIME: self._createtime.isoformat(),
            self.TIMEZONE: self._timezone.zone,
            self.PARTICIPANTS: self._participants
        }
    