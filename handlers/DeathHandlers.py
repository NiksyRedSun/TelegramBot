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
from SomeKeyboards import next_keyb, menu_keyb, death_menu_keyb, next_points_keyb
from SomeAttributes import players_dict, death_tasks_dict
from SomeStates import GameStates, DeathStates
from EasyGameLoader import dp
from SomeClasses.BasicClasses import DeathCounter


async def outrunning_death(message):
    char = players_dict[message.chat.id]
    await asyncio.sleep(2.5)
    while True:
        try:
            await message.answer(text=next(char.deathCounter))
            await asyncio.sleep(2.75)
        except StopIteration:
            if char.deathCounter.check_words():
                char.ressurecting()
                await message.answer(text="Вы вспоминаете всё что с вами случилось и приходите в ужас. Вы были мертвы, "
                                          "а теперь снова живы...", reply_markup=next_points_keyb)
            else:
                await message.answer(text="Вам не удается понять, что произошло. Но, судя по всему, у вас сколько угодно времени. "
                                          "Не похоже, чтобы что-то торопило вас...", reply_markup=next_points_keyb)
                char.deathCounter = None
        except AttributeError:
            pass




@dp.message_handler(state=DeathStates.deadState)
async def death(message: types.Message, state: FSMContext):
    char = players_dict[message.chat.id]
    if message.text == "Попытаться вернуться":
        await message.answer(text="Вы переживаете свою смерть еще раз. Последний момент вашей жизни трудноуловимо мелькает где-то рядом "
                                  "Вы пытаетесь проговорить вслух, всё что происходило с вами перед тем как вы провалились в темноту "
                                  "чтобы понять, что произошло")
        char.get_death_counter()
        death_tasks_dict[message.chat.id] = asyncio.create_task(outrunning_death(message))
        await DeathStates.deadLeftState.set()
    elif message.text == "Персонаж":
        await message.answer(text=char.presentation(), parse_mode="HTML")
    else:
        await message.answer(text="Смерть - это просто часть пути. К счастью вам повезло, "
                              "и в этом мире смерть не является его концом. Вы застряли между миром живых и миром мертвых, "
                              "вам придется раз за разом переживать вашу смерть, пока вы не сумеете её опередить", reply_markup=death_menu_keyb)




@dp.message_handler(state=DeathStates.deadLeftState)
async def try_left_death(message: types.Message, state: FSMContext):
    char = players_dict[message.chat.id]
    if message.text == "Продолжить...":
        if char.alive:
            await message.answer(text="Поначалу немного безумно осозновать то, что с вами произошло. Но спустя некоторое "
                                      "время вы успокаиваетесь и решаете продолжить свой путь", reply_markup=menu_keyb)
            await GameStates.menuState.set()
        else:
            death_tasks_dict[message.chat.id].cancel()
            await message.answer(text="Вы всегда можете попробовать вернуться еще раз", reply_markup=death_menu_keyb)
            await DeathStates.deadState.set()
    else:
        char.deathCounter.check_word(message.text)
