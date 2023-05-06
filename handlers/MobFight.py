# from aiogram import Bot, Dispatcher, types
# from aiogram.utils import executor
# from aiogram.dispatcher.filters.builtin import CommandStart, CommandHelp, Text, IDFilter
# from aiogram.dispatcher.filters import Command
# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ContentType
# from aiogram.dispatcher.storage import FSMContext
# from SomeAttributes import villian
# from SomeStates import GameState
# from EasyGameLoader import dp
# from Functions import next, menu_keyboard
# from SomeAttributes import players_dict
#
#
#
#
#
# async def mob_attack():
#     while True:
#         if not villian.alive:
#             break
#         if check_all_team_dead(current_boss_fight_team):
#             break
#         if not boss_fight_is_on:
#             break
#         await villian.attack_func(current_boss_fight_team, bot)
#         await asyncio.sleep(2)
#         if not villian.alive:
#             break
#         if check_all_team_dead(current_boss_fight_team):
#             break
#         if not boss_fight_is_on:
#             break
#         await asyncio.sleep(2)
#
#
#
# @dp.message_handler(state=GameState.preBossFight)
# async def pre_mob_fight(message: types.Message, state: FSMContext):
#     global boss_fight_is_on, villian
#     if message.text == "Начать бой с боссом":
#         if message.chat.id not in current_boss_fight_team:
#             current_boss_fight_team[message.chat.id] = players_dict[message.chat.id]
#         if message.chat.id not in boss_fight_team:
#             boss_fight_team[message.chat.id] = players_dict[message.chat.id]
#             await message.answer(text=villian.presentation())
#         if not boss_fight_is_on:
#             boss_fight_is_on = True
#             task = asyncio.create_task(boss_attack())
#         await GameState.bossFight.set()
#         await message.answer(text="Что же, в атаку", reply_markup=attack_menu())
#     elif message.text == "Соскочить":
#         await GameState.menuState.set()
#         await message.answer(text="Вы соскакиваете", reply_markup=menu_keyboard())
#     else:
#         menu = ReplyKeyboardMarkup(
#             keyboard=[[KeyboardButton(text="Начать бой с боссом")], [KeyboardButton(text="Соскочить")]], resize_keyboard=True)
#         await message.answer(text="Решите для себя, готовы ли вы\nСпросите у друзей, готовы ли они", reply_markup=menu)
#
#
#
# @rate_limit(limit=0.75)
# @dp.message_handler(state=GameState.bossFight)
# async def mob_fight(message: types.Message, state: FSMContext):
#     global boss_fight_is_on, villian
#     unit = players_dict[message.chat.id]
#     if not villian.alive:
#         await message.answer(text="Ваш противник мертв")
#         await message.answer(text=boss_end(boss_fight_team), reply_markup=next(), parse_mode="HTML")
#         await GameState.menuState.set()
#         await villian.boss_money_exp_dealing(boss_fight_team, message)
#         current_boss_fight_team.clear()
#         boss_fight_team.clear()
#         villian = give_villian()
#         boss_fight_is_on = False
#         return None
#
#     if not unit.alive:
#         await fight_presentantion(unit, villian, message)
#         await message.answer(text="Вы мертвы", reply_markup=next())
#         await GameState.deadState.set()
#     else:
#         await unit.attack_func(villian, message)
#         await fight_presentantion(unit, villian, message)
#
#     if check_all_team_dead(current_boss_fight_team):
#         await message.answer(text="Вся команда нападавших мертва", reply_markup=next())
#         current_boss_fight_team.clear()
#         boss_fight_team.clear()
#         villian = give_villian()
#         boss_fight_is_on = False
#         await GameState.deadState.set()
#
