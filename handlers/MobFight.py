from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.dispatcher.filters.builtin import CommandStart, CommandHelp, Text, IDFilter
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ContentType
from aiogram.dispatcher.storage import FSMContext
from SomeStates import GameState
from EasyGameLoader import dp
from Functions import next, menu_keyboard, give_mobs, give_mobs_links, attack_menu, mob_fight_presentantion, mob_fight_menu
from SomeAttributes import players_dict, mob_fight_dict
from RateLimit import rate_limit, ThrottlingMiddleware
import asyncio


async def mob_check(mob, message):
    while True:
        if not mob.alive:
            await asyncio.sleep(0.15)
            await mob.money_exp_having(players_dict[message.chat.id], message)
            mob_fight_dict[message.chat.id]["mob_task"].cancel()
            mob_fight_dict[message.chat.id]["mob_check_task"].cancel()
            break
        await asyncio.sleep(0.6)


async def mob_attack(mob, message):
    await asyncio.sleep(0.5)
    while True:
        await mob.attack_func(players_dict[message.chat.id], message, )
        await asyncio.sleep(2)



@dp.message_handler(state=GameState.preMobFight)
async def pre_boss_fight(message: types.Message, state: FSMContext):
    if message.text == "Выбрать моба":
        mob_fight_dict[message.chat.id] = {"mob": None, "mob_task": None, "mob_check_task": None, "death_mobs": 0}
        await GameState.mobChoosing.set()
        await message.answer(text="Выбирайте из предложенных")
        await message.answer(text='\n'.join(give_mobs()))
    elif message.text == "Вернуться в деревню":
        await GameState.menuState.set()
        await message.answer(text="Вы возвращаетесь в деревню", reply_markup=menu_keyboard())
    else:
        await message.answer(text="Выбираете противника и в бой", reply_markup=mob_fight_menu())



@dp.message_handler(state=GameState.mobChoosing)
async def pre_boss_fight(message: types.Message, state: FSMContext):
    if message.text in give_mobs_links():
        mob_link = message.text
        mob_fight_dict[message.chat.id]["mob"] = give_mobs(mob_link)
        mob = mob_fight_dict[message.chat.id]["mob"]
        await GameState.mobFight.set()
        await message.answer(text="Вы уже в бою", reply_markup=attack_menu())
        mob_fight_dict[message.chat.id]["mob_task"] = asyncio.create_task(mob_attack(mob, message))
        mob_fight_dict[message.chat.id]["mob_check_task"] = asyncio.create_task(mob_check(mob, message))

    elif message.text == "Вернуться в деревню":
        await GameState.menuState.set()
        await message.answer(text=f"Вы убили {mob_fight_dict[message.chat.id]['death_mobs']} мобов")
        await message.answer(text="Вы возвращаетесь в деревню", reply_markup=menu_keyboard())
        mob_fight_dict.pop(message.chat.id, None)
    else:
        await message.answer(text="Выбирайте моба из предложенных", reply_markup=mob_fight_menu())
        await message.answer(text='\n'.join(give_mobs()))



@rate_limit(limit=1)
@dp.message_handler(state=GameState.mobFight)
async def boss_fight(message: types.Message, state: FSMContext):
    char = players_dict[message.chat.id]
    mob = mob_fight_dict[message.chat.id]['mob']

    if not char.alive:
        await mob_fight_presentantion(char, mob, message)
        await message.answer(text="Вы мертвы", reply_markup=next())
        await message.answer(text=f"Прежде чем умереть, вы убили {mob_fight_dict[message.chat.id]['death_mobs']} мобов", reply_markup=next())
        await GameState.deadState.set()
        mob_fight_dict[message.chat.id]["mob_task"].cancel()
        mob_fight_dict[message.chat.id]["mob_check_task"].cancel()
        mob_fight_dict.pop(message.chat.id, None)
    else:
        if message.text == "Атаковать":
            await char.attack_mob_func(mob, message, mob_fight_dict)
            await mob_fight_presentantion(char, mob, message)
        elif message.text == "Соскочить":
            if await char.leave_mob_fight(mob, message):
                await GameState.mobChoosing.set()
                mob_fight_dict[message.chat.id]["mob_task"].cancel()
                mob_fight_dict[message.chat.id]["mob_check_task"].cancel()
                await message.answer(text="Вы удачно соскакиваете с битвы", reply_markup=next())

        elif message.text == "Продолжить убивать" and not mob.alive:
            await message.answer(text="Вы уже в бою", reply_markup=attack_menu())
            mob_fight_dict[message.chat.id]["mob"].reset()
            mob_fight_dict[message.chat.id]["mob_task"] = asyncio.create_task(mob_attack(mob, message))
            mob_fight_dict[message.chat.id]["mob_check_task"] = asyncio.create_task(mob_check(mob, message))

        elif message.text == "К выбору моба" and not mob.alive:
            await GameState.mobChoosing.set()
            await message.answer(text="Выбирайте моба из предложенных", reply_markup=mob_fight_menu())
            await message.answer(text='\n'.join(give_mobs()))


        else:
            pass
