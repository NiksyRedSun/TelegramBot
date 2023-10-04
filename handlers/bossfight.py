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
from Functions import check_all_team, fight_presentantion, give_villian
from SomeKeyboards import menu_keyb, attack_menu_keyb, next_keyb
from SomeAttributes import current_boss_fight_team, boss_fight_team, players_dict, boss_fight_is_on, boss_fight_is_over, all_items_tnames, all_items_dict
from SomeStates import GameStates, DeathStates
from EasyGameLoader import dp, bot
from threading import Thread
import time
from Functions import check_and_save


async def boss_check_team():
    while True:

        team_state = check_all_team(current_boss_fight_team)
        if team_state == "Left":
            boss_fight_reset()

            break

        elif team_state == "Dead":
            await asyncio.sleep(1)
            for player in current_boss_fight_team.copy():
                await bot.send_message(chat_id=player, text="<b>Вся команда отъехала</b>", parse_mode="HTML")
            boss_fight_reset()
            break

        await asyncio.sleep(0.4)


async def boss_check():
    global boss_fight_is_over
    while True:
        if not villian.alive:
            await asyncio.sleep(1)
            await villian.boss_money_exp_dealing(boss_fight_team, current_boss_fight_team, bot)
            boss_fight_team.clear()
            boss_fight_is_over = True
            task1.cancel()
            break
        await asyncio.sleep(0.65)



def boss_fight_reset():
    global villian, boss_fight_is_over, boss_fight_is_on
    current_boss_fight_team.clear()
    boss_fight_team.clear()
    boss_fight_is_on = False
    boss_fight_is_over = False
    task1.cancel()
    task2.cancel()
    task3.cancel()




async def boss_attack():
    await asyncio.sleep(0.5)
    while True:
        await villian.attack_func(current_boss_fight_team, bot)
        await asyncio.sleep(4)




@dp.message_handler(state=GameStates.preBossFight)
async def pre_boss_fight(message: types.Message, state: FSMContext):
    global boss_fight_is_on, villian, task1, task2, task3
    if message.text == "Начать бой с боссом":
        if not boss_fight_is_on:
            boss_fight_is_on = True
            villian = give_villian()
            task1 = asyncio.create_task(boss_attack())
            task2 = asyncio.create_task(boss_check())
            task3 = asyncio.create_task(boss_check_team())
        if message.chat.id not in current_boss_fight_team:
            current_boss_fight_team[message.chat.id] = {"char": players_dict[message.chat.id], "damage": 0}
        if message.chat.id not in boss_fight_team:
            boss_fight_team[message.chat.id] = players_dict[message.chat.id]
        await message.answer(text=villian.presentation())
        await GameStates.bossFight.set()
        await message.answer(text="Вы уже в бою", reply_markup=attack_menu_keyb)
    elif message.text == "Отказаться от затеи":
        await GameStates.menuState.set()
        await message.answer(text="Вы возвращаетесь в деревню", reply_markup=menu_keyb)
    else:
        if boss_fight_is_over:
            await message.answer(text="Предыдущая сессия боя с боссом еще не окончена, предложите всем игрокам выйти", reply_markup=next_keyb)
            await GameStates.menuState.set()
        else:
            menu = ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text="Начать бой с боссом")], [KeyboardButton(text="Отказаться от затеи")]], resize_keyboard=True)
            await message.answer(text="Решите для себя, готовы ли вы\nСпросите у друзей, готовы ли они", reply_markup=menu)



@rate_limit(limit=1)
@dp.message_handler(state=GameStates.bossFight)
async def boss_fight(message: types.Message, state: FSMContext):
    char = players_dict[message.chat.id]

    if not char.alive:
        await fight_presentantion(char, villian, message)
        await message.answer(text="Вы мертвы", reply_markup=next_keyb)
        await DeathStates.deadState.set()
        current_boss_fight_team.pop(message.chat.id, None)
    else:
        if message.text == "Атаковать":
            await char.attack_boss_func(villian, message, bot, current_boss_fight_team)
            await fight_presentantion(char, villian, message)

        elif message.text == "Сбежать":
            if boss_fight_is_over:
                boss_fight_team.pop(message.chat.id, None)
                current_boss_fight_team.pop(message.chat.id, None)
                await GameStates.menuState.set()
                await message.answer(text="Все и так уже закончилось", reply_markup=menu_keyb)
            if await char.leave_boss_fight(current_boss_fight_team, villian, bot, message) and not boss_fight_is_over:
                boss_fight_team.pop(message.chat.id, None)
                current_boss_fight_team.pop(message.chat.id, None)
                await GameStates.menuState.set()
                await message.answer(text="Вы удачно соскакиваете с битвы", reply_markup=menu_keyb)

        elif message.text == "Инвентарь":
            await char.show_inv_in_fight(message)

        elif message.text == "Уклониться":
            await char.avoid_enemy(message, villian)

        elif message.text in all_items_tnames:
            await all_items_dict[message.text]().item_task(message, char)

        elif message.text == "Закончить":
            if boss_fight_is_over:
                current_boss_fight_team.pop(message.chat.id, None)
                await GameStates.menuState.set()
                await message.answer(text="Вы возвращаетесь в деревню", reply_markup=menu_keyb)
                await char.do_autosave(message)

        else:
            pass







