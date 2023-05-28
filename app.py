import random
import dotenv
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.dispatcher.filters.builtin import CommandStart, CommandHelp, Text, IDFilter
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ContentType
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.storage import FSMContext
from aiogram.utils.exceptions import Throttled
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
import asyncio
from RateLimit import rate_limit, ThrottlingMiddleware
import SomeClasses
from SomeAttributes import players_dict
from SomeStates import GameStates
from EasyGameLoader import dp, bot
from Features import five_second_healing, all_fury_down
import handlers
import time
from threading import Thread
import asyncio





if __name__ == '__main__':
    print("Если ты видишь это сообщение, значит бот в игре")
    loop = asyncio.get_event_loop()
    loop.create_task(all_fury_down(players_dict))
    loop.create_task(five_second_healing(players_dict))
    executor.start_polling(dp)

