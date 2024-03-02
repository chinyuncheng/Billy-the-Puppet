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

from utils import json_helper
import settings

class Language:
    """
    Provide multiple languages to display.
    """
    LANGUAGES_FOLDER = "assets/languages/"

    COMMAND_HELP_DESCRIPTION = "command_help_description"
    COMMAND_HELP_RESULT = "command_help_result"
    COMMAND_HOST_DESCRIPTION = "command_host_description"
    COMMAND_HOST_PARAM_DATE = "command_host_param_date"
    COMMAND_HOST_PARAM_DATE_HINT = "command_host_param_date_hint"
    COMMAND_HOST_PARAM_ENDTIME = "command_host_param_endtime"
    COMMAND_HOST_PARAM_ENDTIME_HINT = "command_host_param_endtime_hint"
    COMMAND_HOST_PARAM_NAME = "command_host_param_name"
    COMMAND_HOST_PARAM_PLAYER = "command_hsot_param_player"
    COMMAND_HOST_PARAM_PLAYER_HINT = "command_host_param_player_hint"
    COMMAND_HOST_PARAM_TIMEZONE = "command_host_param_timezone"
    COMMAND_HOST_PARAM_TIMEZONE_HINT = "command_host_param_timezone_hint"
    COMMAND_HOST_PROCESS = "command_host_process"
    COMMAND_HOST_RECEIVE = "command_host_receive"
    COMMAND_HOST_UPDATE_ERROR = "command_host_update_error"
    COMMAND_LIST_DESCRIPTION = "command_list_description"
    COMMAND_LIST_PARAM_AVAILABLE = "command_list_param_available"
    COMMAND_LIST_PARAM_CREATOR = "command_list_param_creator"
    COMMAND_LIST_RESULT = "command_list_result"
    COMMAND_LIST_RESULT_NOT_FOUND = "command_list_result_not_found"
    COMMAND_MODIFY_DESCRIPTION = "command_modify_description"
    COMMAND_MODIFY_PARAM_LANGUAGE = "command_modify_param_language"
    COMMAND_MODIFY_PARAM_LANGUAGE_HINT = "command_modify_param_language_hint"
    COMMAND_MODIFY_PARAM_TIMEZONE = "command_modify_param_timezone"
    COMMAND_MODIFY_PARAM_TIMEZONE_HINT = "command_modify_param_timezone_hint"
    COMMAND_MODIFY_PROCESS = "command_modify_process"
    COMMAND_MODIFY_RESTRICTION = "command_modify_restriction"
    MESSAGE_HOST_BY = "message_host_by"
    MESSAGE_NO_PARTICIPANTS = "message_no_participants"
    MESSAGE_REACT_TO_JOIN = "message_react_to_join"
    MESSAGE_RECRUITMENT_ENDS = "message_recruitment_ends"
    MESSAGE_RECRUITMENT_ENDS_IN = "message_recruitment_ends_in"
    MESSAGE_REMAINING_TIME_DAYS = "message_remaining_time_days"
    MESSAGE_REMAINING_TIME_DAY = "message_remaining_time_day"
    MESSAGE_REMAINING_TIME_HRS = "message_remaining_time_hrs"
    MESSAGE_REMAINING_TIME_HR = "message_remaining_time_hr"
    MESSAGE_REMAINING_TIME_MINS = "message_remaining_time_mins"
    MESSAGE_REMAINING_TIME_MIN = "message_remaining_time_min"
    MESSAGE_REMAINING_TIME_SECS = "message_remaining_time_secs"
    MESSAGE_REMAINING_TIME_SEC = "message_remaining_time_sec"
    MESSAGE_SLOTS = "message_slots"

    @staticmethod
    def get_languages() -> list[str]:
        """
        Get the list of supported languages
        """
        return [
            "en-us",
            "zh-tw"
        ]

    @staticmethod
    def get_translation(key: str, language: str) -> str:
        """
        Get the translation for a given key and language.
        If the translation is not found, return the key itself.
        """
        path = f"{Language.LANGUAGES_FOLDER}{language}.json"
        lang_data = json_helper.load_without_async(path)
        if not lang_data:
            path = f"{Language.LANGUAGES_FOLDER}{settings.DEFAULT_LANGUAGE}.json"
            lang_data = json_helper.load_without_async(path)

        return lang_data.get(key, key)

    @staticmethod
    def set_user_language(user_id, language):
        """
        Set the preferred language for a user.
        This can be stored in a database or any persistent storage.
        """
        # Implement the logic to store user's preferred language
        pass

    @staticmethod
    def get_user_language(user_id):
        """
        Get the preferred language for a user.
        This retrieves the language stored during language selection.
        """
        # Implement the logic to retrieve user's preferred language
        pass
