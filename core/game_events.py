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
from utils import datetime_helper

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
                 creator: dict, createtime: datetime.datetime, timezone: pytz.tzinfo.BaseTzInfo, participants: dict = None):
        self._name = name
        self._player = player
        self._date = date
        self._endtime = endtime
        self._creator = creator
        self._createtime = createtime
        self._timezone = timezone
        self._participants = participants or {}

    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Value must be a string")
        self._name = value
    
    @property
    def player(self) -> int:
        return self._player
    
    @player.setter
    def player(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Value must be an integer")
        self._player = value
    
    @property
    def date(self) -> datetime.datetime:
        return self._date
    
    @date.setter
    def date(self, value: datetime.datetime):
        if not isinstance(value, datetime.datetime):
            raise TypeError("Value must be a datetime")
        self._date = value
    
    @property
    def endtime(self) -> float:
        return self._endtime

    @endtime.setter
    def endtime(self, value: float):
        if not isinstance(value, float):
            raise TypeError("Value must be a float")
        self._endtime = value
    
    @property
    def creator(self) -> dict:
        return self._creator

    @creator.setter
    def creator(self, value: dict):
        if not isinstance(value, dict):
            raise TypeError("Value must be a dict")
        self._creator = value
    
    @property
    def createtime(self) -> datetime.datetime:
        return self._createtime

    @createtime.setter
    def createtime(self, value: datetime.datetime):
        if not isinstance(value, datetime.datetime):
            raise TypeError("Value must be a datetime")
        self._createtime = value
    
    @property
    def timezone(self) -> pytz.tzinfo.BaseTzInfo:
        return self._timezone

    @timezone.setter
    def timezone(self, value: pytz.tzinfo.BaseTzInfo):
        if not isinstance(value, pytz.tzinfo.BaseTzInfo):
            raise TypeError("Value must be a pytz timezone object")
        self._timezone = value
    
    @property
    def participants(self) -> dict:
        return self._participants

    @participants.setter
    def participants(self, value: dict):
        if not isinstance(value, dict):
            raise TypeError("Value must be a dict")
        self._participants = value

    def _get_messages_creator(self) -> str:
        """
        Get the creator message from current GameEvent instance.
        """
        creator = self.creator[self.CREATOR_DISPLAY_NAME]
        return f"Hosted by {creator} | React to the message to join"

    def _get_messages_date(self) -> str:
        """
        Get the date message from current GameEvent instance.
        """
        sign, offset = datetime_helper.get_timezone_offsets_in_gmt(self.timezone)
        message_date = self.date.strftime('%-m/%d %H:%M')
        message_date += f" GMT{sign}{offset}"

        return message_date

    def _get_messages_participants(self) -> str:
        """
        Get the participants message from current GameEvent instance.
        """
        message_participants = ""
        num_participants = len(self.participants)

        if num_participants > 0:
            participants_list = "\n".join([f"{i+1}. {value}" for i, (_, value) in enumerate(self.participants.items())])
            message_participants += participants_list
        else:
            message_participants = "No participants yet."
        
        return message_participants

    def _get_messages_remaining_time(self) -> str:
        """
        Get the remaining time message from current GameEvent instance.
        """
        is_recruitment_end, remaining_time = self.is_recruitment_end()

        message_remaining_time = "Recruitment ends"
        if not is_recruitment_end:
            days = remaining_time.days
            hours, remainder = divmod(remaining_time.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            message_remaining_time += " in "
            if days > 0:
                message_remaining_time += f"{days} day " if days == 1 else f"{days} days "
            if hours > 0:
                message_remaining_time += f"{hours} hr " if hours == 1 else f"{hours} hrs "
            if minutes > 0:
                message_remaining_time += f"{minutes} min " if minutes == 1 else f"{minutes} mins "
            if seconds > 0:
                message_remaining_time += f"{seconds} sec" if seconds == 1 else f"{seconds} secs"
            message_remaining_time += "\nfrom when this message was sent"

        return message_remaining_time

    def _get_messages_title(self) -> str:
        """
        Get the title message from current GameEvent instance.
        """
        message_date = self._get_messages_date()
        message_slots = self.player - len(self.participants)
        return f"{self.name}  {message_date} [{message_slots} Slots]"

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
            data.get(cls.PARTICIPANTS, {})
        )

    def get_messages(self) -> str:
        """
        Get messages from current GameEvent instance.
        """
        message_title = self._get_messages_title()
        message_remaining_time = self._get_messages_remaining_time()
        message_participants = self._get_messages_participants()
        message_creator = self._get_messages_creator()

        messages = (
            f">>> ## {message_title}\n"
            f"{message_remaining_time}\n"
            f"```\n"
            f"{message_participants}"
            f"```\n"
            f"{message_creator}"
        )

        return messages

    def is_expired(self) -> bool:
        """
        Check if the game event is expired or not.
        """
        now = datetime.datetime.now(tz=self.timezone)
        return now.replace(tzinfo=None) > self.date

    def is_recruitment_end(self) -> tuple[bool, datetime.timedelta]:
        """
        Check if the game event recruitment ends or not.
        """
        now = datetime.datetime.now(tz=self.timezone)
        recruitment_end_time = self.createtime + datetime.timedelta(hours=self.endtime)
        return now > recruitment_end_time or self.is_expired(), recruitment_end_time - now
    
    def is_recruitment_full(self) -> bool:
        """
        Check if the game event recruitment is full or not.
        """
        return len(self.participants) >= self.player

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
