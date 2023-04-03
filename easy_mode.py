import dotenv
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.dispatcher.filters.builtin import CommandStart, CommandHelp
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ContentType

dotenv.load_dotenv()
bot = Bot(token=os.getenv("token"))
dp = Dispatcher(bot)

ids = [372178038, 218656239]

def save_id(message):
    global ids
    if message.chat.id not in ids:
        ids.append(message.chat.id)


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    save_id(message)
    await message.answer(text=f"Ну че, ебаный в рот, погнали нахуй {message.chat.id}")


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Список команд: ",
            "/start - Начать диалог",
            "/help - Получить справку",
            "/menu - Загрузить меню")

    await message.answer("\n".join(text))



@dp.message_handler(Command("show_ids"))
async def show_menu(message: types.Message):
    text = [str(i) for i in ids]
    await message.answer("\n".join(text), parse_mode="HTML")



@dp.message_handler(Command("send_spam"))
async def spam(message):
    global ids
    for i in ids:
        await bot.send_message(i, text="Spam")


@dp.message_handler(Command("menu"))
async def bot_start(message: types.Message):
    menu = ReplyKeyboardMarkup(
        keyboard=[
            [
            KeyboardButton(text="/menu")
            ]
        ],
        resize_keyboard=True
    )
    await message.answer(text="Ну че, ебаный в рот, погнали нахуй", reply_markup=menu)



print("Если ты видишь это сообщение, значит бот в игре")

executor.start_polling(dp)
