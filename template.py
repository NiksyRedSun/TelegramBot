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





@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(text=f"Ну че, погнали народ")



@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Список команд: ",
            "/start - Начать диалог",
            "/help - Получить справку",
            "/menu - Загрузить меню")

    await message.answer("\n".join(text))


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
    await message.answer(text="Ну че, погнали народ", reply_markup=menu)


@dp.message_handler(Text("Просто текст"))
async def bot_help(message: types.Message):
    await message.answer(text="Just text")


@dp.message_handler(Command("test"), state=None) #сюда будут попадать все команды тест, если у них не установлено состояние
async def bot_test(message: types.Message):
    await message.answer(text="Тестирование начато\n"
                              "Вопрос 1\n"
                         "Ответь да или нет?\n"
                         "После отправки этого сообщения я задам тебе как пользователю состояние ответа на первое сообщение\n"
                         "Следующее сообщение будет рассматриваться как твой ответ")
    await Test.Q1.set()


@dp.message_handler(state=Test.Q1) #здесь будет перехват ответа пользователя на первый вопрос, если у пользователя
                                    #есть какое-то состояние, то он попадет только в хэндлер считывания этого состояния
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer1=answer)
    await message.answer(text="Вопрос 2\n"
                         "Реально ну скажи, да или нет \n"
                         "Как только ты ответишь я задам тебе как пользователю состояние ответа на второе сообщение")
    await Test.Q2.set() #переводит состояние пользователя в состояние отправки второго сообщения

@dp.message_handler(state=Test.Q2)
async def answer_q2(message: types.Message, state: FSMContext):
    data = await state.get_data()
    answer1 = data.get("answer1")
    answer2 = message.text
    await message.answer(text=f"Cпасибо за ваши ответы {answer1} и {answer2}")
    await message.answer(text=f"Ответ 1: {answer1}")
    await message.answer(text=f"Ответ 2: {answer2}")

    # await state.finish() # сбрасывается состояние и данные, которые в нем сохранены
    await state.reset_state(with_data=False) #сбросит состояние, но сохранит данные в data


@dp.message_handler(state="EnterEmail") #пример с установлением состояния гораздо более простым способом
async def bot_test2(message: types.Message, state: FSMContext):
    email = message.text
    await state.update_data(email=email)
    await message.answer(text="Ваш мэйл записан")
    await state.reset_state(with_data=False)


@dp.message_handler(Command("test2")) #пример с установлением состояния гораздо более простым способом
async def bot_set_state_test2(message: types.Message, state: FSMContext):
    await message.answer(text="После этого сообщения пользователю будет установлено состояние на отправку мыла")
    await state.set_state("EnterEmail")


@dp.message_handler(Command("mail")) #пример с установлением состояния гораздо более простым способом
async def bot_test2(message: types.Message, state: FSMContext):
    data = await state.get_data()
    email = data.get("email")
    await message.answer(text=f"Ваш мэйл записан: {email}")


print("Если ты видишь это сообщение, значит бот в игре")

executor.start_polling(dp)
