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
        text.append(f"В этом раунде перехватывает инициативу и атакует великий и ужасный {vilian.name}")
        hero_init = double_dices() + hero.initiative
        villian_init = double_dices() + vilian.initiative
        if villian_init > hero_init:
            damage = vilian.attack_damage(text) + dice() - hero.defense
            if damage <= 0:
                text.append(f"Его удар попадает прямо по нашему герою, но тот остается невредим")
            else:
                hero.hp -= damage
                text.append(f"Его удар попадает прямо в цель, нанеся нашему герою {damage} урона")
        else:
            text.append(f"Однако его удар не попадает по цели, наш доблестный герой успевает увернуться")
    else:
        text.append(f"В этом раунде перехватывает инициативу и атакует наш доблестный герой, {hero.name}")
        hero_init = double_dices() + hero.initiative
        villian_init = double_dices() + vilian.initiative
        if hero_init > villian_init:
            damage = hero.attack_damage(text) + dice() - vilian.defense
            if damage <= 0:
                text.append(f"Изловчившись он попадает по противнику, но тот остается невредим")
            else:
                vilian.hp -= damage
                text.append(f"Его точный удар попадает прямо в цель, нанеся противнику {damage} урона")
        else:
            text.append(f"Однако его удар пролетает мимо врага")
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


def death_menu():
    menu = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Вернуться")], [KeyboardButton(text="Персонаж")]], resize_keyboard=True)
    return menu


def check_all_team_dead(players: list, player_dict: dict):
    if all(map(lambda x: not player_dict[x].alive, players)):
        return True
    else:
        return False




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


async def boss_money_dealing(players, enemy, message, players_dict):
    cur_money = int(enemy.money/len(players))
    for i in players:
        players_dict[i].money += cur_money
    await message.answer(text=f"Каждый из участников битвы получил по {cur_money} монет")


async def boss_exp_dealing(players, enemy, message, players_dict):
    cur_exp = int(enemy.exp/len(players))
    for i in players:
        players_dict[i].exp += cur_exp
    await message.answer(text=f"Каждый из участников битвы получил по {cur_exp} опыта")
    for i in players:
        players_dict[i].next_level()


