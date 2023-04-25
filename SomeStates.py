from aiogram.dispatcher.filters.state import StatesGroup, State


class GameState(StatesGroup):
    menuState = State()
    afterChoice = State()
    preBossFight = State()
    bossFight = State()
    deadState = State()
    nameChoice = State()
    charChoice = State()