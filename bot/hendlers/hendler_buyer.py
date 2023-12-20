from aiogram import F, Router
from aiogram.types import Message
from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from keyboards.keyboards import get_key_cancel, get_keyboard_save_and_cancel
from db.engine_db import get_async_session
from db.models import Buyer
from db.states_group import BuyerForm
from utils.crud_operations import create_object
from .start_and_chek_buyer import start_buyer


buyer_router = Router()


@buyer_router.callback_query(F.data == "cancel")
async def cancel(callback: types.CallbackQuery, state: FSMContext):
    """Вызываем старт холдер и чистим конечный автомат"""
    await callback.message.answer("Отмена")
    await state.clear()
    await callback.answer()
    # await start_buyer(callback.message, state)


@buyer_router.callback_query(F.data == "add")
async def input_name(callback: types.CallbackQuery, state: FSMContext):
    """Предлагаем ввести имя"""
    await callback.message.answer("Введи имя клиента", reply_markup=get_key_cancel())
    await state.set_state(BuyerForm.name)
    await callback.answer()


@buyer_router.message(BuyerForm.name)
async def process_name(message: Message, state: FSMContext):
    """Сохраняем имя и предлагаем ввести пленки"""
    await state.update_data(name=message.text)
    await state.set_state(BuyerForm.films)
    await message.answer(
        "Введи пленки которые установил по типу: глянец на дисплей, скин кожа",
        reply_markup=get_key_cancel()
    )


@buyer_router.message(BuyerForm.films)
async def process_films(message: Message, state: FSMContext):
    """Сохраняем типы пленок в автомат и предлагаем ввести суму чека"""
    await state.update_data(films=message.text)
    await state.set_state(BuyerForm.last_cheque)
    await message.answer(
        f"Введи общую сумму чека по типу: 1590",
        reply_markup=get_key_cancel()
    )


@buyer_router.message(BuyerForm.last_cheque, F.text.regexp(r"^[0-9]+$"))
async def process_last_cheque(message: Message, state: FSMContext):
    """Устанавливаем сумму чека и предлагаем сохранить клиента"""
    await state.update_data(last_cheque=int(message.text))
    await state.set_state(BuyerForm.last_cheque)
    data = await state.get_data()

    await message.answer(
        f"Клиент:\nИмя: {data.get('name')}\nНомер: {data.get('number')}\n"
        f"Установленные пленки: {data.get('films')}\n"
        f"Сумма чека: {data.get('last_cheque')}",
        reply_markup=get_keyboard_save_and_cancel()
    )


@buyer_router.message(BuyerForm.last_cheque)
async def last_cheque_incorrectly(message: Message):
    """Вывод сообщения если некоректна введена сумма"""
    await message.answer(
        text="Вводим только цифры"
    )


@buyer_router.callback_query(F.data == "add_obj")
async def save_obj(callback: types.CallbackQuery, state: FSMContext):
    """
    Сохраняем покупателя, очищаем состояние
    и переводим на начало диалога (старт)"""
    await create_object(get_async_session, Buyer, await state.get_data()) 
    await callback.message.answer("Клиент добавлен 👍")
    await state.clear()
    await callback.answer()
    # await start_buyer(callback.message, state)
