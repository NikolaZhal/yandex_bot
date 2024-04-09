import logging
from random import randint

from telegram.ext import Application, MessageHandler, filters
from telegram.ext import CommandHandler, ConversationHandler
from main import logger
from config import BOT_TOKEN
from keyboard import base_markup, close_keyboarder, home_keyboarder, dice_keyboarder, time_keyboarder
from times_commands import time_command, data_command, set_timer, unset


