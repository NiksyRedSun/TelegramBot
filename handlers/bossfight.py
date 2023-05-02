import random
import time

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
from Functions import round, save_id, next, menu_keyboard, attack_menu, boss_end, boss_money_dealing, check_all_team_dead, boss_exp_dealing
from SomeAttributes import villian, pirate, tatarin, viking, elf, khajiit, gnom, ids, units_dict, current_boss_fight_team, players_dict
from SomeStates import GameState
from EasyGameLoader import dp, bot
from threading import Thread
import time



async def boss_attack():
    while True:
        await asyncio.sleep(0.5)
        if current_boss_fight_team:
            await bot.send_message(chat_id=current_boss_fight_team[0], text="Blyad")
        await asyncio.sleep(0.5)
    return None



@dp.message_handler(state=GameState.preBossFight)
async def pre_boss_fight(message: types.Message, state: FSMContext):
    if message.text == "Начать бой с боссом":
        if message.chat.id not in current_boss_fight_team:
            current_boss_fight_team.append(message.chat.id)
        await GameState.bossFight.set()
        task = asyncio.create_task(boss_attack())
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
    await message.answer(text=text)
    if not unit.alive:
        await GameState.deadState.set()
        await message.answer(text="Вы теперь мертв, результаты боя можете узнать у своей команды", reply_markup=next())
        return None
    if not villian.alive:
        await message.answer(text="Ваш противник повержен")
        await message.answer(text=boss_end(current_boss_fight_team, players_dict), reply_markup=next())
        await GameState.menuState.set()
        await boss_money_dealing(current_boss_fight_team, villian, message, players_dict)
        await boss_exp_dealing(current_boss_fight_team, villian, message, players_dict)
        current_boss_fight_team.clear()
        villian.reset()
        return None
    if check_all_team_dead(current_boss_fight_team, players_dict):
        await message.answer(text="Вся команда нападавших мертва")
        current_boss_fight_team.clear()
        villian.reset()
        return None
    menu = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Атаковать")]], resize_keyboard=True)
    await message.answer(text=villian.fight_presentation())
    await message.answer(text=unit.fight_presentation(), reply_markup=menu)




