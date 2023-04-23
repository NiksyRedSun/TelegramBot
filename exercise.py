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


class Test(StatesGroup):
    Q1 = State()
    Q2 = State()


dotenv.load_dotenv()
bot = Bot(token=os.getenv("token"))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)



@dp.message_handler(CommandStart(), state=None)
async def bot_start(message: types.Message):
    await Test.Q1.set()
    await message.answer(text=f"Как к вам можно обращаться?")


@dp.message_handler(state=Test.Q1)
async def bot_second_start(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(login=answer)
    await message.answer(text="Укажите ваш емэйл")
    await Test.Q2.set()


@dp.message_handler(state=Test.Q2)
async def answer_q2(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(email=answer)
    data = await state.get_data()
    login = data.get("login")
    email = data.get("email")
    await message.answer(text=f"Ваш логин: {login} и емэйл: {email}")
    await message.answer(text=f"/menu - чтобы получить меню")
    await state.reset_state(with_data=False)


@dp.message_handler(Command("menu"))
async def bot_start(message: types.Message):
    text = ("<b>Раздел авто</b>",
            "/buy_a - покупка",
            "/sell_a - продажа",
            "/exc_a - обмен",
            "<b>Раздел недвижимости</b>",
            "/buy_n - покупка",
            "/sell_n - продажа",
            "/exc_n - обмен",)
    await message.answer("\n".join(text), parse_mode="HTML")




print("Если ты видишь это сообщение, значит бот в игре")

executor.start_polling(dp)
