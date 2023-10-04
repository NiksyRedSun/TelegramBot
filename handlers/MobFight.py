from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.dispatcher.filters.builtin import CommandStart, CommandHelp, Text, IDFilter
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ContentType
from aiogram.dispatcher.storage import FSMContext
from SomeStates import GameStates, DeathStates
from EasyGameLoader import dp
from Functions import give_mobs, give_mobs_links, mob_fight_presentantion
from SomeKeyboards import next_keyb, end_menu_keyb, attack_menu_keyb, menu_keyb, mob_next_keyb, mob_fight_menu_keyb
from SomeAttributes import players_dict, mob_fight_dict, all_items_dict, all_items_tnames
from RateLimit import rate_limit, ThrottlingMiddleware
import asyncio
from Functions import check_and_save


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
        if message.chat.id not in mob_fight_dict or not players_dict[message.chat.id].alive:
            break
        await mob.attack_func(players_dict[message.chat.id], message)
        await asyncio.sleep(2)



@dp.message_handler(state=GameStates.preMobFight)
async def pre_mob_fight(message: types.Message, state: FSMContext):
    char = players_dict[message.chat.id]
    if message.text == "Выбрать моба":
        mob_fight_dict[message.chat.id] = {"mob": None, "mob_task": None, "mob_check_task": None, "death_mobs": 0}
        await GameStates.mobChoosing.set()
        await message.answer(text="Выбирайте из предложенных")
        await message.answer(text='\n'.join(give_mobs()))

    elif message.text == "Вернуться в деревню":
        await GameStates.menuState.set()
        await message.answer(text="Вы возвращаетесь в деревню", reply_markup=menu_keyb)
        await char.do_autosave(message)
    else:
        await message.answer(text="Выбираете противника и в бой", reply_markup=mob_fight_menu_keyb)



@dp.message_handler(state=GameStates.mobChoosing)
async def mob_choosing(message: types.Message, state: FSMContext):
    char = players_dict[message.chat.id]
    if message.text in give_mobs_links():
        mob_link = message.text
        mob_fight_dict[message.chat.id]["mob"] = give_mobs(mob_link)
        mob = mob_fight_dict[message.chat.id]["mob"]
        await GameStates.mobFight.set()
        await message.answer(text="Вы уже в бою", reply_markup=attack_menu_keyb)
        mob_fight_dict[message.chat.id]["mob_task"] = asyncio.create_task(mob_attack(mob, message))
        mob_fight_dict[message.chat.id]["mob_check_task"] = asyncio.create_task(mob_check(mob, message))

    elif message.text == "Вернуться в деревню":
        await GameStates.menuState.set()
        await message.answer(text=f"Вы убили {mob_fight_dict[message.chat.id]['death_mobs']} мобов")
        await message.answer(text="Вы возвращаетесь в деревню", reply_markup=menu_keyb)
        mob_fight_dict.pop(message.chat.id, None)
        await char.do_autosave()
    else:
        await message.answer(text="Выбирайте моба из предложенных", reply_markup=mob_fight_menu_keyb)
        await message.answer(text='\n'.join(give_mobs()))



@rate_limit(limit=1)
@dp.message_handler(state=GameStates.mobFight)
async def mob_fight(message: types.Message, state: FSMContext):
    char = players_dict[message.chat.id]
    mob = mob_fight_dict[message.chat.id]['mob']

    if not char.alive:
        await mob_fight_presentantion(char, mob, message)
        await message.answer(text="Вы мертвы", reply_markup=next_keyb)
        await message.answer(text=f"Прежде чем умереть, вы убили {mob_fight_dict[message.chat.id]['death_mobs']} мобов", reply_markup=next_keyb)
        await DeathStates.deadState.set()
        mob_fight_dict[message.chat.id]["mob_task"].cancel()
        mob_fight_dict[message.chat.id]["mob_check_task"].cancel()
        mob_fight_dict.pop(message.chat.id, None)
    else:
        if message.text == "Атаковать":
            await char.attack_mob_func(mob, message, mob_fight_dict)
            await mob_fight_presentantion(char, mob, message)
        elif message.text == "Сбежать":
            if await char.leave_mob_fight(mob, message):
                await GameStates.mobChoosing.set()
                mob_fight_dict[message.chat.id]["mob_task"].cancel()
                mob_fight_dict[message.chat.id]["mob_check_task"].cancel()
                await message.answer(text="Вы удачно соскакиваете с битвы", reply_markup=next_keyb)

        elif message.text == "Продолжить убивать" and not mob.alive:
            await message.answer(text="Вы уже в бою", reply_markup=attack_menu_keyb)
            mob_fight_dict[message.chat.id]["mob"].reset()
            mob_fight_dict[message.chat.id]["mob_task"] = asyncio.create_task(mob_attack(mob, message))
            mob_fight_dict[message.chat.id]["mob_check_task"] = asyncio.create_task(mob_check(mob, message))

        elif message.text == "К выбору моба" and not mob.alive:
            await GameStates.mobChoosing.set()
            await message.answer(text="Выбирайте моба из предложенных", reply_markup=mob_fight_menu_keyb)
            await message.answer(text='\n'.join(give_mobs()))
            await char.do_autosave()

        elif message.text == "Инвентарь":
            await char.show_inv_in_fight(message)

        elif message.text == "Уклониться":
            await char.avoid_enemy(message, mob)

        elif message.text in all_items_tnames:
            await all_items_dict[message.text]().item_task(message, char)


        else:
            pass
