from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
from aiogram.dispatcher.filters.builtin import CommandStart, CommandHelp, Text, IDFilter
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ContentType
from EasyGameLoader import dp
from SomeAttributes import players_dict, all_items, all_items_dict, all_items_tnames
from SomeStates import GameStates, ShopStates
from SomeClasses.ItemsClasses import HealingPotion
from SomeKeyboards import menu_keyb
from aiogram.dispatcher.storage import FSMContext



async def assortment(message):
    message_text = []
    for item in all_items:
        message_text.append(item().shop_info())
        message_text.append("")
    await message.answer('\n'.join(message_text))


async def buying_things(message, char, cur_item, count):
    cur_item = all_items_dict[cur_item]()
    if count < 0:
        await message.answer(text="Прикольно вот так вот пытаться ввести отрицательное число на покупку. Не валяй дурака, разъебай")
    elif count == 0:
        await message.answer(text="Ну и иди отсюда, если покупать не хочешь")
    else:
        if char.money >= count * cur_item.cost:
            char.money -= count * cur_item.cost
            char.inventory.extend([cur_item for i in range(count)])
            await message.answer(text=f"Вы закупили {count} единиц данного товара")
        else:
            await message.answer(text="У вас не хватает денег, чтобы купить столько")





@dp.message_handler(state=ShopStates.inShopState)
async def in_shop(message: types.Message, state: FSMContext):
    if message.text in all_items_tnames:
        await state.update_data(needitem=message.text)
        await ShopStates.buyState.set()
        await message.answer(text="Сколько вы хотите приобрести?")
    elif message.text == "Асортимент":
        await assortment(message)
    elif message.text == "В деревню":
        await message.answer(text="Вы возвращаетесь в деревню", reply_markup=menu_keyb, parse_mode="HTML")
        await GameStates.menuState.set()



@dp.message_handler(state=ShopStates.buyState)
async def buy_smth(message: types.Message, state: FSMContext):
    data = await state.get_data()
    cur_item = data.get("needitem")
    char = players_dict[message.chat.id]
    try:
        count = int(message.text)
    except:
        await message.answer(text="Введите корректное значение")
        return None
    await buying_things(message, char, cur_item, count)
    await ShopStates.inShopState.set()


