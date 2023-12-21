from aiogram import F, Router
from aiogram.types import Message
from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from keyboards.keyboards import get_key_cancel, get_keyboard_save_and_cancel, get_keyboard_save_and_cancel_employee, get_yes_no, repeat
from db.engine_db import get_async_session
from db.models import Employee
from db.states_group import EmployeeForm
from utils.crud_operations import create_object, get_object
from .start_and_chek_buyer import start_buyer


admin_router = Router()


@admin_router.callback_query(F.data == "add_employee")
async def input_employee_name(callback: types.CallbackQuery, state: FSMContext):
    """Объявляем состояние и запрашиваем имя и фамилию продавца"""
    await state.clear()
    await callback.message.answer(
        "Введи имя и фамилию продовца через пробел\n"
        "Пример: Иван Иванов",
        reply_markup=get_key_cancel())
    await state.set_state(EmployeeForm.last_name)
    await callback.answer()


async def replay_input_name(message, state):
    await message.answer(
            "Введи имя и фамилию продовца через пробел\n"
        )
    await state.set_state(EmployeeForm.last_name)


def check_name_employee(message: Message):
    first_last_name = message.text.split()
    return len(first_last_name) == 2
        

@admin_router.message(EmployeeForm.last_name)
async def set_name(message: Message, state: FSMContext):
    """Сохраняем имя и предлагаем ввести telegram_id"""
    if not check_name_employee(message):
        await replay_input_name(message, state)
    else:
        first_name, last_name = message.text.split()
        await state.update_data(first_name=first_name, last_name=last_name)
        await state.set_state(EmployeeForm.telegram_id)
        await message.answer(
            "Введи телеграм_id сотрудника, только цифры",
            reply_markup=get_key_cancel()
        )


@admin_router.message(EmployeeForm.telegram_id, F.text.regexp(r"^[0-9]+$"))
async def set_telegram_id(message: Message, state: FSMContext):
    """Сохраняем id в форму и справшиваем делать админом или нет"""
    if await get_object(get_async_session, Employee, "telegram_id", int(message.text)):
        await message.answer(
        "Сотрудник уже добавлен",
        reply_markup=get_key_cancel()
        )
        return 
    await state.update_data(telegram_id=int(message.text))
    await state.set_state(EmployeeForm.is_admin)
    await message.answer(
        "Сделать администратором?",
        reply_markup=get_yes_no()
    )


@admin_router.message(EmployeeForm.telegram_id)
async def incorect_telegram_id(message: Message, state: FSMContext):
    """Если телеграм id введен некоректно"""
    # await state.update_data(telegram_id=int(message.text))
    # await state.set_state(EmployeeForm.is_admin)
    await message.answer(
        "В id должны быть только числа"
    )


@admin_router.callback_query(F.data == "is_admin_true")
async def set_employee_admin(callback: types.CallbackQuery, state: FSMContext):
    """Устанавливаем админом"""
    await state.set_state(EmployeeForm.is_admin)
    await state.update_data(is_admin=True)
    await callback.answer()
    await outout_data_employee(callback, state)


@admin_router.callback_query(F.data == "is_admin_false")
async def outout_data_employee(callback: types.CallbackQuery, state: FSMContext):
    """Выводим введенные данные и предлогаем сохранить"""
    data = await state.get_data()
    print(data)
    await callback.message.answer(
        f"{data.get('last_name')} {data.get('first_name')}\n"
        f"Телеграм_id: {data.get('telegram_id')}\n"
        f"Администратор: {'Да' if data.get('is_admin') else 'Нет'}",
        reply_markup=get_keyboard_save_and_cancel_employee()
    )
    # await state.set_state(EmployeeForm.is_admin)
    # await state.update_data(is_admin=True)
    await callback.answer()


@admin_router.callback_query(F.data == "save_employee")
async def save_employee(callback: types.CallbackQuery, state: FSMContext):
    """Выводим введенные данные и предлогаем сохранить"""
    data = await state.get_data()
    await create_object(get_async_session, Employee, data) 
    await state.clear()
    await callback.answer()
    await callback.message.answer("Сотрудник добавлен 👍", reply_markup=repeat())
