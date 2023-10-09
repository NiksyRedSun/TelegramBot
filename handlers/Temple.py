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
from SomeKeyboards import menu_keyb, attack_menu_keyb, next_keyb, start_keyb, to_vil_keyb
from SomeAttributes import players_dict, current_boss_fight_team
from SomeStates import GameStates
from EasyGameLoader import dp
from SomeRepos.sqlaORM import get_char, delete_char, post_char, put_char
from Functions import check_and_save, check_and_save_stat
from SomeClasses.StatisticsClasses import Statistics



@dp.message_handler(state=GameStates.templeState)
async def temple(message: types.Message, state: FSMContext):
    if message.text == "Сохранить":
        char = players_dict[message.chat.id]
        await check_and_save(char, message)
        await check_and_save_stat(char.stat, message)
        char.stat = Statistics()
    elif message.text == "Загрузить":
        try:
            char = get_char(message.chat.id)
            players_dict[message.chat.id] = char
            await message.answer(text=f"Ваш персонаж {char.name} успешно загружен")
        except:
            await message.answer(text=f"Ваш id не найден в базе данных. Для повторной попытки нажмите на кнопку еще раз")

    elif message.text == "В деревню":
        char = players_dict[message.chat.id]
        await char.do_autosave(message)
        await message.answer(text="Вы возвращаетесь в деревню", reply_markup=menu_keyb, parse_mode="HTML")
        await GameStates.menuState.set()

    elif message.text == "Автосохранение":
        await message.answer(text="Автосохранение автоматически происходит во время возвращения в город", parse_mode="HTML")
        char = players_dict[message.chat.id]
        await char.autosave_switch(message)
    else:
        await message.answer(text=f"Храм позволяет сохранить или загрузить игру, сохранить можно только одного персонажа")

