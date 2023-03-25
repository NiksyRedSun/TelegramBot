from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, bot


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@dp.message_handler(content_types="text", text="/finish")
async def bot_start(message: types.Message):
    await message.answer(text="Финишировал первый забег")


@dp.message_handler(content_types="text")
async def bot_echo(message: types.Message):
    await message.reply(text=message.text)


# Эхо хендлер, куда летят ВСЕ сообщения с указанным состоянием
@dp.message_handler(state="*", content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    state = await state.get_state()
    await message.answer(f"Эхо в состоянии <code>{state}</code>.\n"
                         f"\nСодержание сообщения:\n"
                         f"<code>{message}</code>")
