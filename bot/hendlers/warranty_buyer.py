from datetime import datetime
from aiogram import F, Router, types
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from hendlers.start_and_chek_buyer import start_buyer
from db.models import Buyer
from utils.crud_operations import update_object
from keyboards.keyboards import get_key_cancel, get_keyboard_warranty_save_and_cancel
from db.states_group import BuyerWarrantyForm
from db.engine_db import get_async_session


warranty_router = Router()


@warranty_router.callback_query(F.data == "warranty")
async def cancel(callback: types.CallbackQuery, state: FSMContext):
    """
    Начало диалога 'обращение по гарантии'
    Открываем состояние и спрашиваем тип пленок
    """
    data = await state.get_data()
    number = data.get("number")
    await state.set_state(BuyerWarrantyForm.number)
    await state.update_data(number=number)
    await callback.message.answer(
        "Введи пленки которые установлены",
        reply_markup=get_key_cancel()
    )
    await state.set_state(BuyerWarrantyForm.films)
    await callback.answer()


@warranty_router.message(BuyerWarrantyForm.films)
async def set_film_pointer(message: Message, state: FSMContext) -> None:
    """
    Сохраняем пленки в состояние
    """
    await state.update_data(films=message.text)
    data = await state.get_data()
    
    await message.answer(
        f"Номер: {data.get('number')}\n"
        f"Установленные пленки: {data.get('films')}",
        reply_markup=get_keyboard_warranty_save_and_cancel()
    )

@warranty_router.callback_query(BuyerWarrantyForm.films, F.data == "upd_obj")
async def input_name(callback: types.CallbackQuery, state: FSMContext):
    """Обновляем словарь и вызываем обновление"""
    
    data = await state.get_data()
    data["date_aplication"] = datetime.now()
    await update_object(get_async_session, Buyer, data)
    await callback.message.answer("Выполнено 👍")
    await callback.answer()
    await state.clear()
    await start_buyer(callback.message, state)
