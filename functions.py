import random
from GameClasses import Unit, Villian
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ContentType
from SomeAttributes import villian, pirate, tatarin, viking, elf, khajiit, gnom, ids, units_dict, players_dict


def double_dices():
    return random.randint(1, 6) + random.randint(1, 6)

def dice():
    return random.randint(1, 6)


def round(hero: Unit, vilian: Unit):
    text = []
    hero_init = double_dices() + hero.initiative
    villian_init = double_dices() + vilian.initiative
    if villian_init > hero_init:
        text.append(f"В этом раунде перехватывает инициативу и атакует {vilian.name}")
        hero_init = double_dices() + hero.initiative
        villian_init = double_dices() + vilian.initiative
        if villian_init > hero_init:
            damage = vilian.attack + dice()
            hero.hp -= damage
            text.append(f"Его удар попадает прямо в цель, нанеся {damage} урона")
        else:
            text.append(f"Однако его удар не попадает по цели")
    else:
        text.append(f"В этом раунде перехватывает инициативу и атакует {hero.name}")
        hero_init = double_dices() + hero.initiative
        villian_init = double_dices() + vilian.initiative
        if hero_init > villian_init:
            damage = hero.attack + dice()
            vilian.hp -= damage
            text.append(f"Его удар попадает прямо в цель, нанеся {damage} урона")
        else:
            text.append(f"Однако его удар не попадает по цели")
    return "\n".join(text)



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

def boss_end(players: list, player_dict: dict):
    text = []
    if all(map(lambda x: player_dict[x].alive, players)):
        text.append("+" + "Результаты".center(56, "-") + "+")
        text.append("Вам повезло, все остались в живых")
        text.append("Имена наших героев:")
        for id in players:
            text.append(player_dict[id].name)
        return "\n".join(text)
    else:
        text.append("+" + "Результаты".center(56, "-") + "+")
        text.append("Битва закончена, жаль не все её пережили")
        players.sort(key=lambda x: player_dict[id].alive)
        for id in players:
            if player_dict[id].alive:
                text.append(f"{player_dict[id].name} - Вывез")
            else:
                text.append(f"{player_dict[id].name} - Не вывез")
        return "\n".join(text)


async def money_dealing(players, enemy, message, players_dict):
    if type(players) == list:
        cur_money = int(enemy.money/len(players))
        for i in players:
            players_dict[i].money += cur_money
        await message.answer(text=f"Каждый из участников битвы получил по {cur_money} монет")
    else:
        players.money += enemy.money
        await message.answer(text=f"Монстр обронил {enemy.money} монет после смерти")

