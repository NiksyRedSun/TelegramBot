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
from SomeKeyboards import menu_keyb, person_keyb, person_points_keyb
from SomeAttributes import players_dict, current_boss_fight_team
from SomeStates import GameStates, PersonStates
from EasyGameLoader import dp



@dp.message_handler(state=PersonStates.personMenu)
async def person_menu(message: types.Message, state: FSMContext):
    char = players_dict[message.chat.id]
    if message.text == "Изменить имя":
        await PersonStates.nameChoice.set()
        await message.answer(text="Введите новое имя")
    elif message.text == "Изменить описание":
        await PersonStates.descrChoice.set()
        await message.answer(text="Введите новое описание персонажа")
    elif message.text == "Очки умений":
        await message.answer(text="Здесь можно распределить или перераспределить очки умений:\n"
                                  f"Очков умений у вас: {char.points}\n"
                                  "Атака - 1 очко\n"
                                  "Защита - 1 очко\n"
                                  "Ловкость - 3 очка\n"
                                  "5 hp к максимальному - 1 очко\n", reply_markup=person_points_keyb)
        await PersonStates.personPoints.set()
    elif message.text == "Персонаж":
        await message.answer(text=char.presentation(), parse_mode="HTML")
    elif message.text == "В деревню":
        await message.answer(text="Вы возвращаетесь в деревню", reply_markup=menu_keyb, parse_mode="HTML")
        await GameStates.menuState.set()
    else:
        await message.answer(text="Здесь вы можете изменить имя, описание или перераспределить очки умений")



@dp.message_handler(state=PersonStates.nameChoice)
async def person_name(message: types.Message, state: FSMContext):
    char = players_dict[message.chat.id]
    char.name = message.text
    await message.answer(text=f"Новое имя вашего персонажа: {char.name}")
    await PersonStates.personMenu.set()
    await message.answer(text=char.presentation(), parse_mode="HTML")



@dp.message_handler(state=PersonStates.descrChoice)
async def person_descr(message: types.Message, state: FSMContext):
    char = players_dict[message.chat.id]
    char.story = message.text
    await message.answer(text="Новое описание вашего персонажа готово")
    await PersonStates.personMenu.set()
    await message.answer(text=char.presentation(), parse_mode="HTML")



@dp.message_handler(state=PersonStates.personPoints)
async def person_points(message: types.Message, state: FSMContext):
    char = players_dict[message.chat.id]
    if message.text == "Атака":
        await message.answer(text=f"{char.points_distr('attack')}\n"
                                  f"Очков умений: {char.points}")
        await message.answer(text=char.presentation(), parse_mode="HTML")
    elif message.text == "Защита":
        await message.answer(text=f"{char.points_distr('defense')}\n"
                                  f"Очков умений: {char.points}")
        await message.answer(text=char.presentation(), parse_mode="HTML")
    elif message.text == "Ловкость":
        await message.answer(text=f"{char.points_distr('initiative')}\n"
                                  f"Очков умений: {char.points}")
        await message.answer(text=char.presentation(), parse_mode="HTML")
    elif message.text == "Здоровье":
        await message.answer(text=f"{char.points_distr('hp')}\n"
                                  f"Очков умений: {char.points}")
        await message.answer(text=char.presentation(), parse_mode="HTML")
    elif message.text == "Перераспределить очки":
        await message.answer(text="Вам возвращены ранее потраченные очки")
        await message.answer(text=char.points_distr('reload'))
        await message.answer(text=char.presentation(), parse_mode="HTML")
    elif message.text == "Вернуться":
        await message.answer(text="Не забывайте, что вы получаете новое очко умений"
                                  " каждый 2-ой уровень", reply_markup=person_keyb, parse_mode="HTML")
        await PersonStates.personMenu.set()
    else:
        pass