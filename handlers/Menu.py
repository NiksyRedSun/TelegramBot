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
from SomeKeyboards import menu_keyb, attack_menu_keyb, next_keyb, temple_keyb, person_keyb
from SomeAttributes import players_dict, current_boss_fight_team
from SomeStates import GameStates, PersonStates, DeathStates
from EasyGameLoader import dp




@dp.message_handler(state=GameStates.menuState)
async def villiage(message: types.Message, state: FSMContext):
    char = players_dict[message.chat.id]
    if not char.alive:
        await DeathStates.deadState.set()
        return None
    if message.text == "Бой с боссом":
        await GameStates.preBossFight.set()
        await message.answer(text=f"Попробуйте себя в битве с боссом", reply_markup=next_keyb)
    elif message.text == "Бой с мобом":
        await GameStates.preMobFight.set()
        await message.answer(text=f"Попробуйте себя в очищении мира от мобов", reply_markup=next_keyb)
    elif message.text == "Фонтан":
        await char.fountain_healing(random.randint(1, 6), message)
    elif message.text == "Храм":
        await GameStates.templeState.set()
        await message.answer(text=f"Небольшое деревянное строение, внутри алтари местных божеств.\n"
                                  f"В храме можно cохранить текущего персонажа или загрузить предыдущего записанного",
                             parse_mode="HTML", reply_markup=temple_keyb)
    elif message.text == "Персонаж":
        await message.answer(text=char.presentation(), parse_mode="HTML")
        await message.answer(text="В меню персонажа вы можете поменять имя, описание персонажа,"
                                  " распределить или перераспределить очки умений", parse_mode="HTML",
                             reply_markup=person_keyb)
        await PersonStates.personMenu.set()
    elif message.text in ["Магазин", "Инвентарь"]:
        await message.answer(text=f"Функционал в разработке")
    elif message.text == "Осмотреться":
        looks = ["Вы находитесь на базарной площади небольшого городка",
                 "Здесь очень шумно, хотя людей, казалось бы, не много",
                 "Просто стоите посреди базара и тупите",
                 "Люди на базаре выглядят опасно, но доброжелательно",
                 "Хотя бы солнышко светит",
                 "Висит объявление с предложением поработать в огороде"]
        await message.answer(text=random.choice(looks))
    else:
        await message.answer(text=f"Кто-то называет это место городом, в основном - мэр.\n"
                                  f"Вы и ваши друзья честны друг с другом, поэтому называете это место деревней.\n"
                                  f"Для вас все начинается здесь.\n"
                                  f"Больших путешествий не ждите, в основном всё будет происходить неподалеку.",
                             reply_markup=menu_keyb)
