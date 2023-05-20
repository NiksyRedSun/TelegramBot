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
from SomeKeyboards import menu_keyb, attack_menu_keyb, next_keyb, start_keyb, to_vil_keyb
from SomeAttributes import players_dict, current_boss_fight_team
from SomeStates import StartStates, GameStates
from EasyGameLoader import dp
from SomeRepos.CharsRepo import get_char
from SomeClasses.CharacterClasses import Character


@dp.message_handler(Text("Старт"))
async def bot_start(message: types.Message):
    await message.answer(text=f"Вашему вниманию - мини игра для отдыхающих \n"
                              f"Нажмите 'Начать', чтобы начать\n" 
                              f"Если у вас уже есть персонаж выберете соответствующий пункт меню", reply_markup=start_keyb)
    players_dict[message.chat.id] = None



@dp.message_handler(Text("Начать"), state=None)
async def name_choice(message: types.Message):
    await message.answer(text="Придумайте имя своему персонажу и отправьте его сообщением")
    players_dict[message.chat.id] = Character("Имя", "Описание")
    await StartStates.nameChoice.set()


@dp.message_handler(Text("Есть персонаж"))
async def get_some_char(message: types.Message):
    try:
        char = get_char(message.chat.id)
        players_dict[message.chat.id] = char
        await message.answer(text=char.presentation(), parse_mode="HTML", reply_markup=next_keyb)
        await message.answer(text=f"Ваш персонаж {char.name} успешно загружен")
        await GameStates.menuState.set()
    except:
        await message.answer(text=f"Ваш id не найден в базе данных. Для повторной попытки нажмите на кнопку еще раз\n"
                                  f"Иначе нажмите 'Старт'")


@dp.message_handler(state=StartStates.nameChoice)
async def discr_choice(message: types.Message, state: FSMContext):
    players_dict[message.chat.id].name = message.text
    await message.answer(text="Имя готово, в случае чего, позже можно будет его изменить\n"
                              "А теперь придумайте описание своему персонажу, оно будет отображаться на вашей карточке и видно игрокам\n"
                              "В описании стоит указать расу и класс маги/целители/лучники на текущий момент недоступны")
    await StartStates.descrChoice.set()


@dp.message_handler(state=StartStates.descrChoice)
async def to_villiage(message: types.Message, state: FSMContext):
    players_dict[message.chat.id].story = message.text
    text = players_dict[message.chat.id].presentation()
    await message.answer(text="Здесь начинается ваша история, имя и описание персонажа можно изменить в разделе 'Персонаж'.\n"
                              "Там же можно распределить очки умений, изначально вам доступно 30 очков.\n"
                              "Одно очко умений выдается каждый четный уровень")
    await message.answer(text=text, reply_markup=to_vil_keyb, parse_mode="HTML")
    await GameStates.menuState.set()


