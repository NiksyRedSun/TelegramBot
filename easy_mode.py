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
    await message.answer(text="Ну че, ебаный в рот, погнали нахуй", reply_markup=menu)


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Список команд: ",
            "/start - Начать диалог",
            "/help - Получить справку",
            "/menu - Загрузить меню")

    await message.answer("\n".join(text))


@dp.message_handler(Command("menu"))
async def show_menu(message: types.Message):
    text = ("<b>Аккаунт менеджер</b>",
            "/aqm_forming - Оформление",
            "/admin_qns - Административные вопросы",
            "",
            "<b>Коллер</b>",
            "/taking_calls - Прием звонков",
            "/crm_systems - Ведение CRM системы",
            "",
            "<b>Менеджер вводного урока</b>",
            "/objs - Отработка возражений",
            "/inpl_forming - Оформление",
            "",
            "/marijuana"
            )
    await message.answer("\n".join(text), parse_mode="HTML")


@dp.message_handler(Command("aqm_forming"))
async def aqm_forming(message: types.Message):
    await message.answer(text="Здесь будет информация по оформлению")


@dp.message_handler(Command("admin_qns"))
async def admin_qns(message: types.Message):
    await message.answer(text="Здесь будет информация по административным вопросам")


@dp.message_handler(Command("taking_calls"))
async def taking_calls(message: types.Message):
    await message.answer(text="Здесь будет информация по приему звонков")


@dp.message_handler(Command("crm_systems"))
async def crm_systems(message: types.Message):
    await message.answer(text="Здесь будет информация по ведению CRM систем")


@dp.message_handler(Command("objs"))
async def objs(message: types.Message):
    await message.answer(text="Здесь будет информация по отработке возражений")


@dp.message_handler(Command("inpl_forming"))
async def inpl_forming(message: types.Message):
    await message.answer(text="Здесь будет информация по оформлению")


@dp.message_handler(Command("marijuana"))
async def marijuana(message: types.Message):
    sticker = open("C:\\repos\\tg_bot\\mj.webp", "rb")
    await bot.send_sticker(message.chat.id, sticker)


@dp.message_handler()
async def get_message(message: types.Message):
    chat_id = message.chat.id
    text = "Some_text"
    await message.answer(text=text)


print("Если ты видишь это сообщение, значит бот в игре")

executor.start_polling(dp)
