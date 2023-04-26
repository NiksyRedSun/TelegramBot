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
from Functions import round, save_id, next, menu_keyboard
from SomeAttributes import villian, pirate, tatarin, viking, elf, khajiit, gnom, ids, units_dict, players_dict, testChar
from SomeStates import GameState
from EasyGameLoader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    save_id(message, ids)
    menu = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Старт")]], resize_keyboard=True, one_time_keyboard=True)
    await message.answer(text=f"Вашему вниманию - мини игра для отдыхающих \n"
                              f"Нажмите на старт, чтобы начать", reply_markup=menu)
    players_dict[message.chat.id] = None


@dp.message_handler(Text("Старт"), state=None)
async def bot_choice(message: types.Message):
    await message.answer(text="Выберите персонажа:\n"
                              "/pirate - пират\n"
                              "/tatarin - татарин\n"
                              "/viking - викинг\n"
                              "/elf - эльф\n"
                              "/khajiit - каджит\n"
                              "/gnom - гном\n"
                              "/testChar - под тест\n")
    await GameState.charChoice.set()


@dp.message_handler(state=GameState.charChoice)
async def after_choice(message: types.Message, state: FSMContext):
    players_dict[message.chat.id] = units_dict[message.text]
    await GameState.nameChoice.set()
    await message.answer(text="Придумайте себе имя, отправьте его сообщением")


@dp.message_handler(state=GameState.nameChoice)
async def after_choice(message: types.Message, state: FSMContext):
    players_dict[message.chat.id].name = message.text
    text = players_dict[message.chat.id].presentation()
    menu = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="В меню")]], resize_keyboard=True)
    await message.answer(text=text, reply_markup=menu)
    await GameState.menuState.set()


@dp.message_handler(state=GameState.menuState)
async def before_fight(message: types.Message, state: FSMContext):
    if message.text == "Бой с боссом":
        await GameState.preBossFight.set()
        await message.answer(text=f"Попробуйте себя в битве с боссом", reply_markup=next())
        await message.answer(text=villian.presentation(), reply_markup=next())
    elif message.text == "Персонаж":
        text = players_dict[message.chat.id].presentation()
        await message.answer(text=text)
    elif message.text in ["Бой с мобом", "Магазин", "Инвентарь"]:
        await message.answer(text=f"Функционал в разработке")
    else:
        await message.answer(text=f"Выберите чем хотите заниматься", reply_markup=menu_keyboard())