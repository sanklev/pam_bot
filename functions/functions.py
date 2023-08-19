import logging
import aiogram as aio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State
from aiogram.dispatcher.filters.state import StatesGroup
from os import getenv
from sys import exit
import aiogram.utils.markdown as md
from aiogram.types import ParseMode
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text

def compel_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Принять")
    keyboard.add('Отказаться')
    keyboard.add('Обсудить')
    return keyboard

def send_master_text(bot, master, data, text):
    bot.send_message(chat_id=master, text=md.text(
        md.text(f"{md.bold(data['user'])}, {text}")
        # sep='\n',
    ),
                     parse_mode=ParseMode.MARKDOWN,
                     )
