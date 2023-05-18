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
from Functions import charChoosing
from SomeKeyboards import menu_keyb, attack_menu_keyb, next_keyb, start_keyb, vil_keyb
from SomeAttributes import players_dict, current_boss_fight_team
from SomeStates import GameState
from EasyGameLoader import dp
from SomeRepos.CharsRepo import get_char, delete_char, post_char



@dp.message_handler(state=GameState.templeState)
async def villiage(message: types.Message, state: FSMContext):
    if message.text == "Сохранить":
        char = players_dict[message.chat.id]
        delete_char(message.chat.id)
        await message.answer(text=post_char(message.chat.id, char))
    elif message.text == "Загрузить":
        char = get_char(message.chat.id)
        if char is not None:
            players_dict[message.chat.id] = char
            await message.answer(text=f"Ваш персонаж {char.name} успешно загружен")
        else:
            await message.answer(text=f"Ваш id не найден в базе данных. Для повторной попытки нажмите на кнопку еще раз")
    elif message.text == "В деревню":
        await message.answer(text="Вы возвращаетесь в деревню", reply_markup=vil_keyb, parse_mode="HTML")
        await GameState.menuState.set()
    else:
        await message.answer(text=f"Храм позволяет сохранить или загрузить игру, сохранить можно только одного персонажа")

