import random
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ContentType
from GameClasses import Character, Villian, SpiderVillian, DragonVillian, GolemVillian, TreeVillian


def double_dices():
    return random.randint(1, 6) + random.randint(1, 6)


def dice():
    return random.randint(1, 6)


def save_id(message, ids):
    if message.chat.id not in ids:
        ids.append(message.chat.id)


def next():
    menu = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Продолжить")]], resize_keyboard=True)
    return menu


def menu_keyboard():
    menu = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Бой с боссом"), KeyboardButton(text="Бой с мобом")],
                  [KeyboardButton(text="Магазин"), KeyboardButton(text="Инвентарь")], [KeyboardButton(text="Персонаж")]], resize_keyboard=True)
    return menu


def attack_menu():
    menu = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Атаковать")]], resize_keyboard=True)
    return menu


def death_menu():
    menu = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Вернуться")], [KeyboardButton(text="Персонаж")]], resize_keyboard=True)
    return menu





def check_all_team_dead(players: dict):
    if all(map(lambda x: not players[x].alive, players)):
        return True
    else:
        return False


def boss_end(players: dict):
    text = []
    text.append("<code>+" + "Результаты".center(30, "-") + "+</code>")
    text.append("Имена наших героев:")
    for id in players:
        text.append(players[id].name)
    return "\n".join(text)


async def boss_money_dealing(players: dict, enemy, message):
    cur_money = int(enemy.money/len(players))
    for i in players:
        players[i].money += cur_money
    await message.answer(text=f"Каждый из участников битвы получил по {cur_money} монет")


async def boss_exp_dealing(players:dict, enemy, message):
    cur_exp = int(enemy.exp/len(players))
    for i in players:
        players[i].exp += cur_exp
    await message.answer(text=f"Каждый из участников битвы получил по {cur_exp} опыта")
    for i in players:
        players[i].next_level()


def charChoosing(text):
    match text:
        case "/pirate":
            return Character("Черная борода", "Как вы уже догадались, вы пират", 45, 5, 3, 4)
        case "/tatarin":
            return Character("Айзулбек", "Вы тут за татарина с луком", 25, 8, 3, 4)
        case "/viking":
            return Character("Сигурд", "Вы тут за викинга, вам ничего не остается кроме как махать мечом", 60, 10, 4, 2)
        case "/elf":
            return Character("Дарриан", "Вы тут за эльфа, наемного убийцу", 20, 8, 1, 6)
        case "/khajiit":
            return Character("Рисаад", "Опция для тех, кто хочет играть за каджита", 30, 7, 1, 5)
        case "/gnom":
            return Character("Эдукан", "Никакой команде не обойтись без гнома, на вас - размахивать топором", 50, 8, 4, 3)
        case "/testChar":
            return Character("SomePers", "Используем этого перса для тестирования", 1000, 1000, 1000, 1000)


async def fight_presentantion(char, enemy, message):
    line = ""
    line += char.fight_presentation() + "\n"
    line += "\n" * 2
    # line += "<code>" + "=" * 31 + "</code>" + "\n"
    line += enemy.fight_presentation()
    await message.answer(text=line, reply_markup=attack_menu(), parse_mode="HTML")

def give_villian():
    return random.choice([DragonVillian(), SpiderVillian(), GolemVillian(), TreeVillian()])