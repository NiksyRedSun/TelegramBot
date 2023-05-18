from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ContentType


next_keyb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Продолжить")]], resize_keyboard=True)


menu_keyb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Бой с боссом"), KeyboardButton(text="Бой с мобом")],
              [KeyboardButton(text="Магазин"), KeyboardButton(text="Инвентарь")], [KeyboardButton(text="Персонаж")],
              [KeyboardButton(text="Фонтан"), KeyboardButton(text="Храм")]], resize_keyboard=True)


attack_menu_keyb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Атаковать")], [KeyboardButton(text="Соскочить")]], resize_keyboard=True)

end_menu_keyb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Закончить")]], resize_keyboard=True)



death_menu_keyb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Вернуться")], [KeyboardButton(text="Персонаж")]], resize_keyboard=True)

mob_fight_menu_keyb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Выбрать моба")], [KeyboardButton(text="Вернуться в деревню")]],
    resize_keyboard=True)


mob_next_keyb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Продолжить убивать")], [KeyboardButton(text="К выбору моба")]],
    resize_keyboard=True)

start_keyb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Старт")], [KeyboardButton(text="Есть персонаж")]], resize_keyboard=True, one_time_keyboard=True)

vil_keyb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="В деревню")]], resize_keyboard=True)


temple_keyb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Сохранить")], [KeyboardButton(text="Загрузить")], [KeyboardButton(text="В деревню")]], resize_keyboard=True)