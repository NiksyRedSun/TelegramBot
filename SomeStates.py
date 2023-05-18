from aiogram.dispatcher.filters.state import StatesGroup, State


class GameState(StatesGroup):
    menuState = State()

    preBossFight = State()
    bossFight = State()

    deadState = State()

    nameChoice = State()
    charChoice = State()

    preMobFight = State()
    mobFight = State()
    mobChoosing = State()

    templeState = State()