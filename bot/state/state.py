from aiogram.dispatcher.filters.state import State, StatesGroup


class ChoiceWinner(StatesGroup):
    winner_id = State()


class EditCasinoText(StatesGroup):
    text = State()


class EditActionsText(StatesGroup):
    text = State()


class Cart(StatesGroup):
    user_id = State()
    bar = State()
    time = State()
    phone = State()
    name = State()
    cart = State()
    page = State()
