import dotenv
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor                  # импорт екзекутера

dotenv.load_dotenv()
bot = Bot(token=os.getenv("token"))                 # создание бота
dp = Dispatcher(bot)                                # создаем диспатчер, передаем бота


@dp.message_handler()                               # хэндлер, позволяет принимать текстовые сообщения
async def get_message(message: types.Message):
    chat_id = message.chat.id
    # text = "Some_text"
    # sent_message = await bot.send_message(chat_id=chat_id, text=text)       # await нужен, потому что все завязано на
                                                    # асинхронности, send_message - метод, отправляет сообщение от бота,
                                                    # sent_message - нужен чтобы добраться до результата отправки сообщения
    bot_user = await bot.get_me()
    print(bot_user.username)



# bot.get_updates()  # получить апдейты
executor.start_polling(dp)  # собирает все апдейты, чтобы их куда-то передавать, нужно прописать handler, для хэндлера
# нужен dispatcher