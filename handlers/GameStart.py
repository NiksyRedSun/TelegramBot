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
from SomeRepos.CharsRepo import get_char


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(text=f"Вашему вниманию - мини игра для отдыхающих \n"
                              f"Нажмите на старт, чтобы начать\n" 
                              f"Если у вас уже есть персонаж выберете соответствующий пункт меню", reply_markup=start_keyb)
    players_dict[message.chat.id] = None



@dp.message_handler(Command("restart"), state=None)
async def re_char_choice(message: types.Message):
    await message.answer(text="Выберите персонажа:\n"
                              "/pirate - пират\n"
                              "/tatarin - татарин\n"
                              "/viking - викинг\n"
                              "/elf - эльф\n"
                              "/khajiit - каджит\n"
                              "/gnom - гном\n"
                              "/testChar - под тест\n")
    await GameState.charChoice.set()




@dp.message_handler(Text("Старт"), state=None)
async def char_choice(message: types.Message):
    await message.answer(text="Выберите персонажа:\n"
                              "/pirate - пират\n"
                              "/tatarin - татарин\n"
                              "/viking - викинг\n"
                              "/elf - эльф\n"
                              "/khajiit - каджит\n"
                              "/gnom - гном\n"
                              "/testChar - под тест\n")
    await GameState.charChoice.set()


@dp.message_handler(Text("Есть персонаж"))
async def get_some_char(message: types.Message):
    char = get_char(message.chat.id)
    if char is not None:
        players_dict[message.chat.id] = char
        text = players_dict[message.chat.id].presentation()
        await message.answer(text=f"Ваш персонаж {char.name} успешно загружен")
        await message.answer(text=text, reply_markup=vil_keyb, parse_mode="HTML")
        await GameState.menuState.set()
    else:
        await message.answer(text=f"Ваш id не найден в базе данных. Для повторной попытки нажмите на кнопку еще раз,"
                                  f" иначе нажмите 'Старт'")



@dp.message_handler(state=GameState.charChoice)
async def name_choice(message: types.Message, state: FSMContext):
    players_dict[message.chat.id] = charChoosing(message.text)
    await GameState.nameChoice.set()
    await message.answer(text="Придумайте себе имя, отправьте его сообщением")


@dp.message_handler(state=GameState.nameChoice)
async def to_villiage(message: types.Message, state: FSMContext):
    players_dict[message.chat.id].name = message.text
    text = players_dict[message.chat.id].presentation()
    await message.answer(text=text, reply_markup=vil_keyb, parse_mode="HTML")
    await GameState.menuState.set()


