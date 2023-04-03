import tkinter as tk
import random
import dotenv
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.dispatcher.filters.builtin import CommandStart, CommandHelp
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ContentType

root = tk.Tk()
root.geometry("300x600")

action = ''

dotenv.load_dotenv()
bot = Bot(token=os.getenv("token"))
dp = Dispatcher(bot)

ids = [372178038, 218656239]


async def buy():
    global ids
    pass


async def sell():
    global ids
    for i in ids:
        await bot.send_message(i, text="Продажа")


def change():
    global ids
    async def change():
        for i in ids:
            await bot.send_message(i, text="Обмен")
    change()


some_val = 0


button1 = tk.Button(text='Покупка', background='DodgerBlue3', font='Arial 15', command=buy)
button1.pack()

button2 = tk.Button(text='Продажа', background='DodgerBlue3', font='Arial 15', command=sell)
button2.pack()

button3 = tk.Button(text='Обмен', background='DodgerBlue3', font='Arial 15', command=change)
button3.pack()


root.mainloop()


