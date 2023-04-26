from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.dispatcher.filters.builtin import CommandStart, CommandHelp, Text, IDFilter
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ContentType
from aiogram.dispatcher.storage import FSMContext
from SomeAttributes import villian, pirate, tatarin, viking, elf, khajiit, gnom, ids, units_dict
from SomeStates import GameState
from EasyGameLoader import dp




@dp.message_handler(Text("Бой с мобом"))
async def start_fight(message: types.Message):
    await message.answer(text="Функционал в разработке")

