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

import discord
import logging
import os
from dotenv import load_dotenv
from logging.config import dictConfig

load_dotenv()

CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GAME_EVENTS_FILE_PATH = "game_events.json"
GAME_EVENTS_DELETION_PERIOD_IN_HOURS = 72
GUILD_ID = discord.Object(id=int(os.getenv("GUILD_ID")))
LANGUAGE = "zh-tw"
TIMEZONE = "Asia/Taipei"

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "[%(asctime)s] [%(levelname)-7s] %(name)s: %(message)s"
        },
        "verbose": {
            "format": "[%(asctime)s] [%(levelname)-7s] %(module)s: %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "DEBUG",
        },
        "console2": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "WARNING",
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "verbose",
            "filename": "logs/info.log",
            "level": "INFO"
        },
        "error_file": {
            "class": "logging.FileHandler",
            "formatter": "verbose",
            "filename": "logs/error.log",
            "level": "ERROR"
        }
    },
    "loggers": {
        "bot": {
            "handlers": ["console", "file", "error_file"],
            "level": "INFO",
            "propagate": False
        },
        "discord": {
            "handlers": ["console2", "file", "error_file"],
            "level": "INFO",
            "propagate": False
        },
    }
}

dictConfig(LOGGING_CONFIG)
