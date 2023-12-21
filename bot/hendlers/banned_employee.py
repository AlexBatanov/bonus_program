from aiogram import F, Router
from aiogram.types import Message
from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from hendlers.add_employee import check_name_employee
from keyboards.keyboards import get_key_cancel, get_keyboard_banned_employee, get_keyboard_save_and_cancel, get_keyboard_save_and_cancel_employee, get_yes_no, repeat
from db.engine_db import get_async_session
from db.models import Employee
from db.states_group import EmployeeBanForm
from utils.crud_operations import create_object, get_object, update_object
from .start_and_chek_buyer import start_buyer


banned_employee = Router()

@banned_employee.callback_query(F.data == "ban_employee")
async def input_employee_tg(callback: types.CallbackQuery, state: FSMContext):
    """Объявляем состояние и запрашиваем имя и фамилию продавца"""
    await state.clear()
    await callback.message.answer(
        "Введи телеграм_id сотрудника\n",
        reply_markup=get_key_cancel())
    await state.set_state(EmployeeBanForm.telegram_id)
    await callback.answer()


@banned_employee.message(EmployeeBanForm.telegram_id, F.text.regexp(r"^[0-9]+$"))
async def output_employee_name(message: Message, state: FSMContext):
    """Сохраняем имя и предлагаем ввести telegram_id"""
    employee = await get_object(get_async_session, Employee, "telegram_id", int(message.text))
    if not employee:
        await message.answer("Сотрудник не найден", reply_markup=get_key_cancel())
    else:
        await state.update_data(telegram_id=int(message.text))
        await message.answer(
            f"Заблокировать {employee.last_name} {employee.first_name}?",
            reply_markup=get_keyboard_banned_employee()
        )

@banned_employee.message(EmployeeBanForm.telegram_id)
async def incorect_telegram_id(message: Message, state: FSMContext):
    """Если телеграм id введен некоректно"""
    await message.answer(
        "В id должны быть только числа"
    )


@banned_employee.callback_query(F.data == "banned_employee")
async def banned_employee_name(callback: types.CallbackQuery, state: FSMContext):
    """Сохраняем имя и предлагаем ввести telegram_id"""
    data = await state.get_data()
    employee = await get_object(get_async_session, Employee, "telegram_id", data.get("telegram_id"))
    data["is_banned"] = True
    await update_object(get_async_session, employee, data)
    await callback.message.answer("Сотрудник заблокирован", reply_markup=repeat())
    await callback.answer()
