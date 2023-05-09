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
from Functions import next, menu_keyboard, death_menu
from SomeAttributes import players_dict
from SomeStates import GameState
from EasyGameLoader import dp



@dp.message_handler(state=GameState.deadState)
async def after_choice(message: types.Message, state: FSMContext):
    char = players_dict[message.chat.id]
    if message.text == "Вернуться":
        await message.answer(text="Вас восстанавливает", reply_markup=menu_keyboard())
        await GameState.menuState.set()
        char.ressurecting()
    elif message.text == "Персонаж":
        text = players_dict[message.chat.id].presentation()
        await message.answer(text=text, parse_mode="HTML")
    else:
        await message.answer(text="Смерть - это просто часть пути. К счастью вам повезло, "
                              "и в этом мире смерть не является его концом.", reply_markup=death_menu())