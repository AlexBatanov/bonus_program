from aiogram.filters.state import StatesGroup, State


class BuyerForm(StatesGroup):
    number = State()
    name = State()
    films = State()
    last_cheque = State()
    last_employee = State()

class BuyerUpdateForm(StatesGroup):
    number = State()
    name = State()
    films = State()
    last_cheque = State()
    bonus_points = State()
    last_employee = State()

class BuyerWarrantyForm(StatesGroup):
    films = State()
    number = State()

class EmployeeForm(StatesGroup):
    telegram_id = State()
    first_name = State()
    last_name = State()
    is_admin = State()

class EmployeeBanForm(StatesGroup):
    telegram_id = State()