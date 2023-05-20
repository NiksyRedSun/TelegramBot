from aiogram.dispatcher.filters.state import StatesGroup, State


class GameStates(StatesGroup):
    menuState = State()

    preBossFight = State()
    bossFight = State()

    deadState = State()

    preMobFight = State()
    mobFight = State()
    mobChoosing = State()

    templeState = State()


class StartStates(StatesGroup):
    nameChoice = State()
    descrChoice = State()


class PersonStates(StatesGroup):
    personMenu = State()
    nameChoice = State()
    descrChoice = State()
    personPoints = State()