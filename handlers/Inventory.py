from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
from aiogram.dispatcher.filters.builtin import CommandStart, CommandHelp, Text, IDFilter
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ContentType
from EasyGameLoader import dp


@dp.message_handler(Text("Инвентарь"))
async def start_fight(message: types.Message):
    await message.answer(text="Функционал в разработке")