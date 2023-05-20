import random
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ContentType
from SomeClasses.CharacterClasses import Character
from SomeClasses.VillianClasses import Villian, TreeVillian, GolemVillian, DragonVillian, SpiderVillian, WyvernVillian
from SomeClasses.MobClasses import SceletonMob, LittleDragonMob, OrcMob
from SomeKeyboards import attack_menu_keyb, menu_keyb, end_menu_keyb, mob_next_keyb, next_keyb



def double_dices():
    return random.randint(1, 6) + random.randint(1, 6)


def dice():
    return random.randint(1, 6)



def check_all_team(players: dict):
    if len(players) == 0:
        return "Left"
    if all(map(lambda x: not players[x]["char"].alive, players)):
        return "Dead"
    else:
        return "Alive"


async def show_players(players: dict, message):
    pass



def charChoosing(text):
    match text:
        case "/pirate":
            return Character("Черная борода", "Как вы уже догадались, вы пират", 45, 5, 3, 4)#29
        case "/tatarin":
            return Character("Айзулбек", "Вы тут за татарина с луком", 25, 8, 3, 4)#28
        case "/viking":
            return Character("Сигурд", "Вы тут за викинга, вам ничего\n не остается кроме как махать\n мечом", 55, 10, 4, 2)#31
        case "/elf":
            return Character("Дарриан", "Вы тут за эльфа, наемного убийцу", 20, 8, 1, 6)#31
        case "/khajiit":
            return Character("Рисаад", "Опция для тех, кто хочет играть за каджита", 30, 7, 1, 5)#29
        case "/gnom":
            return Character("Эдукан", "Никакой команде не обойтись без\n гнома, на вас - размахивать\n топором", 50, 8, 4, 3)#31
        case "/testChar":
            return Character("SomePers", "Используем этого перса для тестирования", 1000, 100, 100, 100)


async def fight_presentantion(char, enemy, message):
    line = ""
    line += char.fight_presentation() + "\n"
    line += "\n" * 2
    # line += "<code>" + "=" * 31 + "</code>" + "\n"
    line += enemy.fight_presentation()
    if enemy.alive:
        await message.answer(text=line, reply_markup=attack_menu_keyb, parse_mode="HTML")
    else:
        await message.answer(text=line, reply_markup=end_menu_keyb, parse_mode="HTML")


async def mob_fight_presentantion(char, mob, message):
    line = ""
    line += char.fight_presentation() + "\n"
    line += "\n" * 2
    # line += "<code>" + "=" * 31 + "</code>" + "\n"
    line += mob.fight_presentation()
    if mob.alive and char.alive:
        await message.answer(text=line, reply_markup=attack_menu_keyb, parse_mode="HTML")
    else:
        if char.alive:
            await message.answer(text=line, reply_markup=mob_next_keyb, parse_mode="HTML")
        else:
            await message.answer(text=line, reply_markup=next_keyb, parse_mode="HTML")


def give_villian():
    return random.choice([DragonVillian(), SpiderVillian(), GolemVillian(), TreeVillian(), WyvernVillian()])


def give_mobs(mob_link=None):
    mobs_list = [SceletonMob(), LittleDragonMob(), OrcMob()]
    if mob_link is None:
        text = []
        for mob in mobs_list:
            text.append(f"{mob.link} - {mob.name}\n{mob.story}\n")
        return text
    else:
        match mob_link:
            case "/SceletonMob":
                return SceletonMob()
            case "/LittleDragonMob":
                return LittleDragonMob()
            case "/OrcMob":
                return OrcMob()


def give_mobs_links():
    mobs_list = [SceletonMob(), LittleDragonMob(), OrcMob()]
    result_list = []
    for mob in mobs_list:
        result_list.append(mob.link)
    return result_list
