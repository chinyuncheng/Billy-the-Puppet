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

import pytz

class GuildInfo:
    """
    The guild information class for saving details.
    """
    GUILD_INFO_JSON = "guild_infos.json"
    ROOT_FOLDER = "assets/guilds/"

    ID = "id"
    LANGUAGE = "language"
    PATH = "path"
    TIMEZONE = "timezone"

    def __init__(self, id: str, path: str, language: str, timezone: pytz.tzinfo.BaseTzInfo):
        self._id = id
        self._path = path
        self._language = language
        self._timezone = timezone

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Value must be a string")
        self._id = value

    @property
    def path(self) -> str:
        return self._path

    @path.setter
    def path(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Value must be a string")
        self._path = value

    @property
    def language(self) -> str:
        return self._language

    @language.setter
    def language(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Value must be a string")
        self._language = value

    @property
    def timezone(self) -> pytz.tzinfo.BaseTzInfo:
        return self._timezone

    @timezone.setter
    def timezone(self, value: pytz.tzinfo.BaseTzInfo):
        if not isinstance(value, pytz.tzinfo.BaseTzInfo):
            raise TypeError("Value must be a pytz timezone object")
        self._timezone = value

    @classmethod
    def from_dict(cls, data: dict):
        """
        Get Guild instance from dict
        """
        return cls(
            data[cls.ID],
            data[cls.PATH],
            data[cls.LANGUAGE],
            pytz.timezone(data[cls.TIMEZONE]),
        )

    def get_game_event_json_path(self, channel_id: int) -> str:
        """
        Get the JSON file path for saving GameEvent data
        """
        return f"{self.path}/{channel_id}.json"

    def get_json_path(self) -> str:
        """
        Get the JSON file path of this GuildInfo
        """
        return f"{self.path}/{GuildInfo.GUILD_INFO_JSON}"

    def to_dict(self):
        """
        Convert Guild instance to dict.
        """
        return {
            self.ID: self._id,
            self.PATH: self._path,
            self.LANGUAGE: self._language,
            self.TIMEZONE: self._timezone.zone,
        }
