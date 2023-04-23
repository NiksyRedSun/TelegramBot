import random
from GameClasses import Unit, Villian
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ContentType
from SomeAttributes import villian, pirate, tatarin, viking, elf, khajiit, gnom, ids, units_dict, alive_players, death_players, players


def round(hero: Unit, vilian: Unit):
    text = []
    hero_init = random.randint(1, 6) + hero.initiative
    villian_init = random.randint(1, 6) + vilian.initiative
    if villian_init > hero_init:
        text.append(f"В этом раунде перехватывает инициативу и атакует {vilian.name}")
        hero_init = random.randint(1, 6) + hero.initiative
        villian_init = random.randint(1, 6) + vilian.initiative
        if villian_init > hero_init:
            damage = vilian.attack + random.randint(1, 6)
            hero.hp -= damage
            text.append(f"Его удар попадает прямо в цель, нанеся {damage} урона")
        else:
            text.append(f"Однако его удар не попадает по цели")
    else:
        text.append(f"В этом раунде перехватывает инициативу и атакует {hero.name}")
        hero_init = random.randint(1, 6) + hero.initiative
        villian_init = random.randint(1, 6) + vilian.initiative
        if hero_init > villian_init:
            damage = hero.attack + random.randint(1, 6)
            vilian.hp -= damage
            text.append(f"Его удар попадает прямо в цель, нанеся {damage} урона")
        else:
            text.append(f"Однако его удар не попадает по цели")
    return "\n".join(text)


async def restart_message(message):
    menu = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="/restart")]], resize_keyboard=True)
    await message.answer(text="/restart - чтобы попробовать еще раз",
                         reply_markup=menu)

def save_id(message, ids):
    if message.chat.id not in ids:
        ids.append(message.chat.id)