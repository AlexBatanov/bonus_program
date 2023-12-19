from aiogram.filters.state import StatesGroup, State


class BuyerForm(StatesGroup):
    number = State()
    name = State()
    films = State()
    last_cheque = State()
    employe = State()

class BuyerUpdateForm(StatesGroup):
    number = State()
    name = State()
    films = State()
    last_cheque = State()
    bonus_points = State()
    employe = State()

class BuyerWarrantyForm(StatesGroup):
    films = State()
    number = State()