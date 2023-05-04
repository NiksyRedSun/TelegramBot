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
from Functions import save_id, next, menu_keyboard, attack_menu, boss_end, boss_money_dealing, check_all_team_dead, boss_exp_dealing, fight_presentantion, give_villian
from SomeAttributes import villian, pirate, tatarin, viking, elf, khajiit, gnom, ids, units_dict, current_boss_fight_team, boss_fight_team, players_dict, boss_fight_is_on
from SomeStates import GameState
from EasyGameLoader import dp, bot
from threading import Thread
import time


async def boss_attack():
    while True:
        await villian.attack_func(current_boss_fight_team, bot)
        await asyncio.sleep(4)
        if not villian.alive:
            break
        if check_all_team_dead(current_boss_fight_team):
            break
        if not boss_fight_is_on:
            break



@dp.message_handler(state=GameState.preBossFight)
async def pre_boss_fight(message: types.Message, state: FSMContext):
    global boss_fight_is_on
    if message.text == "Начать бой с боссом":
        if message.chat.id not in current_boss_fight_team:
            current_boss_fight_team[message.chat.id] = players_dict[message.chat.id]
        if message.chat.id not in boss_fight_team:
            boss_fight_team[message.chat.id] = players_dict[message.chat.id]
            await message.answer(text=villian.presentation())
        if not boss_fight_is_on:
            boss_fight_is_on = True
            task = asyncio.create_task(boss_attack())
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
    global boss_fight_is_on, villian
    unit = players_dict[message.chat.id]
    if check_all_team_dead(current_boss_fight_team):
        await message.answer(text="Вся команда нападавших мертва", reply_markup=next())
        current_boss_fight_team.clear()
        boss_fight_team.clear()
        boss_fight_is_on = False
        await GameState.deadState.set()
        return None
    if not unit.alive:
        await GameState.deadState.set()
        await fight_presentantion(unit, villian, message)
        await message.answer(text="Вы мертвы", reply_markup=next())
        del current_boss_fight_team[message.chat.id]
        return None
    if not villian.alive:
        await message.answer(text="Ваш противник мертв")
        await message.answer(text=boss_end(boss_fight_team), reply_markup=next(), parse_mode="HTML")
        await GameState.menuState.set()
        await boss_money_dealing(boss_fight_team, villian, message)
        await boss_exp_dealing(boss_fight_team, villian, message)
        current_boss_fight_team.clear()
        boss_fight_team.clear()
        villian = give_villian()
        boss_fight_is_on = False
        return None
    await unit.attack_func(villian, message)
    await fight_presentantion(unit, villian, message)




