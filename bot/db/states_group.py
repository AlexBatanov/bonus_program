from aiogram.filters.state import StatesGroup, State


class BuyerForm(StatesGroup):
    number = State()
    name = State()
    films = State()
    last_cheque = State()