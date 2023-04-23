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
from functions import round, restart_message, save_id
from SomeAttributes import villian, pirate, tatarin, viking, elf, khajiit, gnom, ids, units_dict, alive_players, death_players, players
from SomeStates import Test


dotenv.load_dotenv()
bot = Bot(token=os.getenv("token"))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(ThrottlingMiddleware())



@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    save_id(message, ids)
    menu = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Старт")]], resize_keyboard=True, one_time_keyboard=True)
    await message.answer(text=f"Вашему вниманию - мини игра для отдыхающих \n"
                              f"Нажмите на старт, чтобы начать", reply_markup=menu)



@dp.message_handler(Text("Старт"), state=None)
async def bot_choice(message: types.Message):
    await message.answer(text="Выберите персонажа:\n"
                              "/pirate - пират\n"
                              "/tatarin - татарин\n"
                              "/viking - викинг\n"
                              "/elf - эльф\n"
                              "/khajiit - каджит\n"
                              "/gnom - гном\n")
    await Test.Q1.set()



print("Если ты видишь это сообщение, значит бот в игре")

executor.start_polling(dp)
