from aiogram.filters.state import StatesGroup, State


class BuyerForm(StatesGroup):
    number = State()
    name = State()
    films = State()
    last_cheque = State()
    employee = State()

class BuyerUpdateForm(StatesGroup):
    number = State()
    name = State()
    films = State()
    last_cheque = State()
    bonus_points = State()
    employee = State()

class BuyerWarrantyForm(StatesGroup):
    films = State()
    number = State()