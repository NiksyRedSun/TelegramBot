import dotenv
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor      # импорт екзекутера
from aiogram.dispatcher.filters.builtin import CommandStart, CommandHelp
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

dotenv.load_dotenv()
bot = Bot(token=os.getenv("token"))                 # создание бота
dp = Dispatcher(bot)                                # создаем диспатчер, передаем бота


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    menu = ReplyKeyboardMarkup(
        keyboard=[
            [
            KeyboardButton(text="/menu")
            ]
        ],
        resize_keyboard=True
    )
    await message.answer(text="Стартуем", reply_markup=menu)


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Список команд: ",
            "/start - Начать диалог",
            "/help - Получить справку",
            "/menu - Загрузить меню")

    await message.answer("\n".join(text))


@dp.message_handler(Command("menu"))
async def show_menu(message: types.Message):

    await message.answer()


@dp.message_handler()                               # хэндлер, позволяет принимать текстовые сообщения
async def get_message(message: types.Message):
    chat_id = message.chat.id
    text = "Some_text"
    # sent_message = await bot.send_message(chat_id=chat_id, text=text)       # await нужен, потому что все завязано на
    await message.answer(text=text)     # асинхронности, send_message - метод, отправляет сообщение от бота,
    # sent_message - нужен чтобы добраться до результата отправки сообщения
    # await message.answer(text=text) как аналог await bot.send_message(chat_id=chat_id, text=text)


print("Если ты видишь это сообщение, значит бот в игре")

executor.start_polling(dp)  # собирает все апдейты, чтобы их куда-то передавать, нужно прописать handler, для хэндлера
# нужен dispatcher
