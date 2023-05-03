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
from GameClasses import Unit, Villian
from Functions import check_all_team_dead
from SomeAttributes import villian, pirate, tatarin, viking, elf, khajiit, gnom, ids, units_dict, current_boss_fight_team
from SomeStates import GameState
from EasyGameLoader import dp, bot
import handlers
import time
from threading import Thread
import asyncio





if __name__ == '__main__':
    print("Если ты видишь это сообщение, значит бот в игре")
    executor.start_polling(dp)

