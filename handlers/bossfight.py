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
import SomeClasses
from Functions import next, menu_keyboard, attack_menu, check_all_team, fight_presentantion, give_villian
from SomeAttributes import villian, current_boss_fight_team, boss_fight_team, players_dict, boss_fight_is_on, boss_fight_is_over
from SomeStates import GameState
from EasyGameLoader import dp, bot
from threading import Thread
import time



def boss_fight_reset():
    global villian, boss_fight_is_over, boss_fight_is_on
    current_boss_fight_team.clear()
    boss_fight_team.clear()
    boss_fight_is_on = False
    boss_fight_is_over = False
    villian = give_villian()



async def boss_attack():
    global boss_fight_is_over
    while True:
        if not villian.alive:
            await villian.boss_money_exp_dealing(boss_fight_team, bot)
            boss_fight_is_over = True
            break

        team_state = check_all_team(current_boss_fight_team)
        if team_state in ["Left", "Dead"]:
            break
        if not boss_fight_is_on:
            break

        await villian.attack_func(current_boss_fight_team, bot)
        await asyncio.sleep(2)

        if not villian.alive:
            await villian.boss_money_exp_dealing(boss_fight_team, bot)
            boss_fight_is_over = True
            break

        team_state = check_all_team(current_boss_fight_team)
        if team_state in ["Left", "Dead"]:
            break
        if not boss_fight_is_on:
            break
        await asyncio.sleep(2)



@dp.message_handler(state=GameState.preBossFight)
async def pre_boss_fight(message: types.Message, state: FSMContext):
    global boss_fight_is_on, villian
    if message.text == "Начать бой с боссом":
        if not boss_fight_is_on:
            boss_fight_is_on = True
            task = asyncio.create_task(boss_attack())
        if message.chat.id not in current_boss_fight_team:
            current_boss_fight_team[message.chat.id] = players_dict[message.chat.id]
        if message.chat.id not in boss_fight_team:
            boss_fight_team[message.chat.id] = players_dict[message.chat.id]
        await message.answer(text=villian.presentation())
        await GameState.bossFight.set()
        await message.answer(text="Что же, в атаку", reply_markup=attack_menu())
    elif message.text == "Соскочить":
        await GameState.menuState.set()
        await message.answer(text="Вы соскакиваете", reply_markup=menu_keyboard())
    else:
        if boss_fight_is_over:
            await message.answer(text="Предыдущая сессия боя с боссом еще не окончена, предложите всем игрокам выйти", reply_markup=next())
            await GameState.menuState.set()
        else:
            menu = ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text="Начать бой с боссом")], [KeyboardButton(text="Соскочить")]], resize_keyboard=True)
            await message.answer(text="Решите для себя, готовы ли вы\nСпросите у друзей, готовы ли они", reply_markup=menu)



@rate_limit(limit=0.75)
@dp.message_handler(state=GameState.bossFight)
async def boss_fight(message: types.Message, state: FSMContext):
    char = players_dict[message.chat.id]
    if not villian.alive:
        await GameState.menuState.set()
        current_boss_fight_team.pop(message.chat.id, None)
        await message.answer(text="Ваш противник мертв", reply_markup=next(), parse_mode="HTML")

    if not char.alive:
        await fight_presentantion(char, villian, message)
        await message.answer(text="Вы мертвы", reply_markup=next())
        await GameState.deadState.set()
        current_boss_fight_team.pop(message.chat.id, None)
    else:
        if message.text == "Атаковать":
            await char.attack_func(villian, message)
            await fight_presentantion(char, villian, message)
        elif message.text == "Соскочить":
            if await char.leave_boss_fight(current_boss_fight_team, villian, bot, message, message.chat.id):
                boss_fight_team.pop(message.chat.id, None)
                boss_fight_team.pop(message.chat.id, None)
                await GameState.menuState.set()
                await message.answer(text="Вы удачно соскакиваете с битвы", reply_markup=menu_keyboard())
        else:
            pass

    team_state = check_all_team(current_boss_fight_team)
    if team_state == "Left":
        boss_fight_reset()

    elif team_state == "Dead":
        await message.answer(text="Вся команда нападавших мертва", reply_markup=next())
        boss_fight_reset()
        await GameState.deadState.set()







