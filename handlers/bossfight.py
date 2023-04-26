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
from Functions import round, save_id, next, menu_keyboard, attack_menu, boss_end, money_dealing
from SomeAttributes import villian, pirate, tatarin, viking, elf, khajiit, gnom, ids, units_dict, current_boss_fight_team, players_dict
from SomeStates import GameState
from EasyGameLoader import dp



@dp.message_handler(state=GameState.preBossFight)
async def pre_boss_fight(message: types.Message, state: FSMContext):
    if message.text == "Начать бой с боссом":
        if message.chat.id not in current_boss_fight_team:
            current_boss_fight_team.append(message.chat.id)
        await GameState.bossFight.set()
        await message.answer(text="Что же, в атаку", reply_markup=attack_menu())
    elif message.text == "Соскочить":
        await GameState.menuState.set()
        await message.answer(text="Вы соскакиваете", reply_markup=menu_keyboard())
    else:
        menu = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Начать бой с боссом")], [KeyboardButton(text="Соскочить")]], resize_keyboard=True)
        await message.answer(text="Решите для себя, готовы ли вы\nСпросите у друзей, готовы ли они", reply_markup=menu)



@rate_limit(limit=0.75)
@dp.message_handler(state=GameState.bossFight)
async def boss_fight(message: types.Message, state: FSMContext):
    unit = players_dict[message.chat.id]
    text = round(unit, villian)
    villian.check_alive()
    unit.check_alive()
    if not unit.alive:
        await GameState.deadState.set()
        await message.answer(text="Вы теперь мертв, результаты боя можете узнать у своей команды", reply_markup=next())
        return None
    if not villian.alive:
        await message.answer(text="Ваш противник повержен")
        await message.answer(text=boss_end(current_boss_fight_team, players_dict), reply_markup=next())
        await GameState.menuState.set()
        await money_dealing(current_boss_fight_team, villian, message, players_dict)
        current_boss_fight_team.clear()
        villian.reset()
        return None
    menu = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Атаковать")]], resize_keyboard=True)
    await message.answer(text=text)
    await message.answer(text=villian.fight_presentation())
    await message.answer(text=unit.fight_presentation(), reply_markup=menu)




