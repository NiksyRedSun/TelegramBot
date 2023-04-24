from aiogram.dispatcher.filters.state import StatesGroup, State


class GameState(StatesGroup):
    menuState = State()
    Q2 = State()