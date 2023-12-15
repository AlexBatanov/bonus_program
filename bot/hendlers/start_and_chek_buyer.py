from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from keyboards.keyboards import get_keyboard_find_buyer, get_keyboard_not_find_duyer
from db.engine_db import get_async_session
from utils.crud_operations import get_object
from db.models import Buyer
from db.states_group import BuyerForm


start_buyer_router = Router()


@start_buyer_router.message(CommandStart())
async def start_buyer(message: Message, state: FSMContext):
    """Начало работы бота"""
    await state.set_state(BuyerForm.number)
    await message.answer(
        "Введи номер клиента в формате: 89271112233",
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
        await message.answer(
            f"Имя: {obj.name}\n"
            f"Дата посещения: {obj.date_aplication.strftime('%d.%m.%Y')}\n"
            f"Доступно бонусов: {obj.bonus_points}\n"
            f"Количество установок: {obj.count_aplications}\n"
            f"Наклеенные пленки: {obj.films}\n"
            f"Сумма последнего чека: {obj.last_cheque}\n",
            reply_markup=get_keyboard_find_buyer()
        )
    else:
        await message.answer(
            "Клиент не найден, добавить?",
            reply_markup=get_keyboard_not_find_duyer()
        )
