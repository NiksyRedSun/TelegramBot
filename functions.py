import random
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ContentType
from SomeClasses.CharacterClasses import Character
from SomeClasses.VillianClasses import Villian, TreeVillian, GolemVillian, DragonVillian, SpiderVillian



def double_dices():
    return random.randint(1, 6) + random.randint(1, 6)


def dice():
    return random.randint(1, 6)



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



def check_all_team(players: dict):
    if len(players) == 0:
        return "Left"
    if all(map(lambda x: not players[x].alive, players)):
        return "Dead"
    else:
        return "Alive"



def charChoosing(text):
    match text:
        case "/pirate":
            return Character("Черная борода", "Как вы уже догадались, вы пират", 45, 5, 3, 4)
        case "/tatarin":
            return Character("Айзулбек", "Вы тут за татарина с луком", 25, 8, 3, 4)
        case "/viking":
            return Character("Сигурд", "Вы тут за викинга, вам ничего\n не остается кроме как махать\n мечом", 60, 10, 4, 2)
        case "/elf":
            return Character("Дарриан", "Вы тут за эльфа, наемного убийцу", 20, 8, 1, 6)
        case "/khajiit":
            return Character("Рисаад", "Опция для тех, кто хочет играть за каджита", 30, 7, 1, 5)
        case "/gnom":
            return Character("Эдукан", "Никакой команде не обойтись без\n гнома, на вас - размахивать\n топором", 50, 8, 4, 3)
        case "/testChar":
            return Character("SomePers", "Используем этого перса для тестирования", 1, 1, 1, 1)


async def fight_presentantion(char, enemy, message):
    line = ""
    line += char.fight_presentation() + "\n"
    line += "\n" * 2
    # line += "<code>" + "=" * 31 + "</code>" + "\n"
    line += enemy.fight_presentation()
    if enemy.alive:
        await message.answer(text=line, reply_markup=attack_menu(), parse_mode="HTML")
    else:
        await message.answer(text=line, reply_markup=end_menu(), parse_mode="HTML")

def give_villian():
    return random.choice([DragonVillian(), SpiderVillian(), GolemVillian(), TreeVillian()])