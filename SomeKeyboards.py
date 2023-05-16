from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ContentType


def next():
    menu = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Продолжить")]], resize_keyboard=True)
    return menu


def menu_keyboard():
    menu = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Бой с боссом"), KeyboardButton(text="Бой с мобом")],
                  [KeyboardButton(text="Магазин"), KeyboardButton(text="Инвентарь")], [KeyboardButton(text="Персонаж")],
                  [KeyboardButton(text="Фонтан")]], resize_keyboard=True)
    return menu


def attack_menu():
    menu = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Атаковать")], [KeyboardButton(text="Соскочить")]], resize_keyboard=True)
    return menu

def end_menu():
    menu = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Закончить")]], resize_keyboard=True)
    return menu


def death_menu():
    menu = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Вернуться")], [KeyboardButton(text="Персонаж")]], resize_keyboard=True)
    return menu

def mob_fight_menu():
    menu = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Выбрать моба")], [KeyboardButton(text="Вернуться в деревню")]],
        resize_keyboard=True)
    return menu


def mob_next():
    menu = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Продолжить убивать")], [KeyboardButton(text="К выбору моба")]],
        resize_keyboard=True)
    return menu

