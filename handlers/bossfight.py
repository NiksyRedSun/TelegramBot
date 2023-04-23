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
from functions import round, restart_message
from SomeAttributes import villian, pirate, tatarin, viking, elf, khajiit, gnom, ids, units_dict, alive_players, death_players, players
from SomeStates import Test
from EasyGame import dp



@dp.message_handler(state=Test.Q1)
async def before_fight(message: types.Message, state: FSMContext):
    global players
    await state.update_data(unit=units_dict[message.text])
    players = players + 1
    data = await state.get_data()
    text = data.get("unit").presentation()
    await state.reset_state(with_data=False)
    await message.answer(text=text)
    await message.answer(text=villian.presentation())
    menu = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Начать бой")]], resize_keyboard=True, one_time_keyboard=True)
    await message.answer(text=f"Нажмите на кнопку \"Начать бой\", когда все будут готовы", reply_markup=menu)



@dp.message_handler(Text("Начать бой"))
async def start_fight(message: types.Message, state: FSMContext):
    data = await state.get_data()
    menu = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Атаковать")]], resize_keyboard=True)
    await message.answer(text=villian.fight_presentation())
    await message.answer(text=data.get("unit").fight_presentation(), reply_markup=menu)


@rate_limit(limit=0.75)
@dp.message_handler(Text("Атаковать"))
async def attack(message: types.Message, state: FSMContext):
    data = await state.get_data()
    unit = data.get("unit")
    text = round(unit, villian)
    villian.check_alive()
    unit.check_alive()
    if not unit.alive:
        await Test.Q2.set()
        death_players.append(unit.name)
        await message.answer(text=text)
        await message.answer(text="В общем-то вы отъехали, ожидайте завершения боя")
        menu = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="/vil_alive")]], resize_keyboard=True)
        await message.answer(text="/vil_alive - проверить жив ли злодей", reply_markup=menu)
        return None
    if not villian.alive:
        alive_players.append(unit.name)
        if death_players:
            text = "Злодей побежден " + ", ".join(alive_players) + " - при этом остались в живых\n" + ", ".join(death_players) + " - мертвы, да упокоятся их души"
            await message.answer(text=text)
            await restart_message(message)
        else:
            text = "Похоже героям сегодня удалось победить злодея.\nВот они слева направо: " + ", ".join(alive_players)
            await message.answer(text=text)
            await restart_message(message)
        return None
    await state.update_data(unit=unit)
    menu = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Атаковать")]], resize_keyboard=True)
    await message.answer(text=text)
    await message.answer(text=villian.fight_presentation())
    await message.answer(text=data.get("unit").fight_presentation(), reply_markup=menu)


@dp.message_handler(state=Test.Q2 or Command("vil_alive"))
async def check_villian(message: types.Message, state: FSMContext):
    villian.check_alive()
    if not villian.alive:
        if death_players:
            text = "Злодей побежден " + ", ".join(alive_players) + " - при этом остались в живых, " + \
                   ", ".join(death_players) + "мертвы, да упокоятся их души"
            await state.reset_state()
            await message.answer(text=text)
            await restart_message(message)
            return None
        else:
            text = "Похоже героям сегодня удалось победить злодея.\nВот они слева направо: " + ", ".join(alive_players)
            await state.reset_state()
            await message.answer(text=text)
            await restart_message(message)
            return None
    if len(death_players) == players:
        await message.answer(text="Все просто поотъезжали, ну и все")
        await state.reset_state()
        await restart_message(message)
        return None
    await message.answer(text="Злодей все еще жив")
    await message.answer(text="/vil_alive проверить злодея еще раз")


@dp.message_handler(Command("restart"))
async def restart(message: types.Message, state: FSMContext):
    global players, villian
    alive_players.clear()
    death_players.clear()
    players = 0
    villian = Villian("Груда костей", "Несколько тысяч костей, по прикидкам в нем человек 10, не меньше", 200, 7, 4)
    await state.reset_state()
    menu = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Старт")]], resize_keyboard=True, one_time_keyboard=True)
    await message.answer(text=f"Вашему вниманию - мини игра для отдыхающих \n"
                              f"Нажмите на старт, чтобы начать", reply_markup=menu)
