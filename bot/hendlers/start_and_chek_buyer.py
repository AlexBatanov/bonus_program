from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode, chat_type

from keyboards.keyboards import (get_keyboard_find_buyer,
                                 get_keyboard_not_find_duyer, get_keybords_add_del_employee)
from db.engine_db import get_async_session
from utils.crud_operations import get_object
from db.models import Buyer, Employee
from db.states_group import BuyerForm


start_buyer_router = Router()

@start_buyer_router.callback_query(F.data == "cancel")
@start_buyer_router.message(CommandStart())
async def start_buyer(message: Message | CallbackQuery, state: FSMContext):
    """Начало работы бота"""

    if type(message) is CallbackQuery:
        await state.clear()

    employee_id = message.from_user.id
    print()
    print(employee_id)
    print()
    await state.set_state(BuyerForm.last_employee)
    await state.update_data(last_employee=employee_id)
    obj = await get_object(get_async_session, Employee, 'telegram_id', employee_id)
    # if True:
    if obj and obj.is_admin:
        await state.set_state(BuyerForm.number)
        await message.answer(
            "Введи номер клиента в формате: 89271112233",
            reply_markup=get_keybords_add_del_employee(),
        )
    elif obj and not obj.is_banned:
        await state.set_state(BuyerForm.number)
        await message.answer(
            "Введи номер клиента в формате: 89271112233",
        )
    else:
        await message.answer(
            "Для работы с ботом отправь администратору\n"
            f"свой id <code><b>{employee_id}</b></code>",
            parse_mode=ParseMode.HTML
        )


@start_buyer_router.message(BuyerForm.number, F.text.regexp(r"\d{11}"))
async def check_buyer(message: Message, state: FSMContext):
    """
    Проверяем существование покупателя
    Если нет, то переходим к диалогу создания
    иначе открываем диалог работы с клиентом
    """
    await state.update_data(number=message.text)

    obj = await get_object(get_async_session, Buyer, 'number', message.text)
    if obj:
        employee = await get_object(get_async_session, Employee, 'telegram_id', obj.last_employee)
        await message.answer(
            f"Имя: {obj.name}\n"
            f"Дата посещения: {obj.date_aplication.strftime('%d.%m.%Y')}\n"
            f"Доступно бонусов: {obj.bonus_points}\n"
            f"Количество установок: {obj.count_aplications}\n"
            f"Наклеенные пленки: {obj.films}\n\n"
            f"Продавец: {employee.last_name} {employee.first_name}\n"
            f"Сумма последнего чека: {obj.last_cheque}\n",
            reply_markup=get_keyboard_find_buyer()
        )
    else:
        await state.update_data(number=int(message.text))
        await message.answer(
            "Клиент не найден, добавить?",
            reply_markup=get_keyboard_not_find_duyer()
        )
