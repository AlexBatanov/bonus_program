from aiogram import F, Router, types
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from utils.helpers import set_data_buyer_sale
from hendlers.start_and_chek_buyer import start_buyer
from keyboards.keyboards import get_key_cancel, get_keyboard_sale_save_and_cancel, repeat
from db.engine_db import get_async_session
from utils.crud_operations import get_object, update_object
from db.models import Buyer
from db.states_group import BuyerForm, BuyerUpdateForm


sale_buyer_router = Router()


@sale_buyer_router.callback_query(F.data == "sale")
async def input_films(callback: types.CallbackQuery, state: FSMContext):
    """
    Объявлем конечный автомат обнавления покупателя
    Запрашиваем установленые пленки
    """
    data = await state.get_data()
    number = data.get("number")
    await state.set_state(BuyerUpdateForm.number)
    await state.update_data(number=number)
    await callback.message.answer(
        "Введи пленки которые установил по типу: глянец на дисплей, скин кожа",
        reply_markup=get_key_cancel()
    )
    await state.set_state(BuyerUpdateForm.films)
    await callback.answer()


@sale_buyer_router.message(BuyerUpdateForm.films)
async def set_film_pointer(message: Message, state: FSMContext) -> None:
    """
    Сохраняем пленки в состояние
    """
    
    await state.update_data(films=message.text)
    await message.answer(
        f"Введи общую сумму чека по типу: 1590",
        reply_markup=get_key_cancel()
    )
    await state.set_state(BuyerUpdateForm.last_cheque)


@sale_buyer_router.message(BuyerUpdateForm.last_cheque, F.text.regexp(r"^[0-9]+$"))
async def process_last_cheque(message: Message, state: FSMContext):
    """Устанавливаем сумму чека и предлагаем сохранить клиента"""

    await state.update_data(last_cheque=int(message.text))
    await state.set_state(BuyerForm.last_cheque)
    await input_count_bonus(message, state)


async def input_count_bonus(message, state):
    data = await state.get_data()
    buyer = await get_object(get_async_session, Buyer, "number", data.get('number'))
    bonus = buyer.bonus_points
    await message.answer(
        f"Доступно баллов: {bonus}\nВведи сколько списать от 0 до {bonus}",
        reply_markup=get_key_cancel()
    )
    await state.set_state(BuyerUpdateForm.bonus_points)


async def chek_correct_bonus(message, state):
    """Проверяем на корректность введенных баллов"""
    data = await state.get_data()
    buyer = await get_object(get_async_session, Buyer, "number", data.get('number'))
    bonus = buyer.bonus_points
    if int(message.text) > bonus:
        await message.answer(
            f"Максимальное количесвто для списания {bonus}"
        )
        await input_count_bonus(message, state)


@sale_buyer_router.message(BuyerUpdateForm.bonus_points, F.text.regexp(r"^[0-9]+$"))
async def set_bonus_pointer(message: Message, state: FSMContext):
    """Сохраняем баллы в состояние"""
    await chek_correct_bonus(message, state)
    await state.update_data(bonus_points=int(message.text))
    await saly_ouput_data(message, state)

@sale_buyer_router.message(BuyerUpdateForm.last_cheque)
async def incorect_cheque(message, state):
    await message.answer("Вводим только числа")
    await state.set_state(BuyerUpdateForm.last_cheque)


@sale_buyer_router.message(BuyerUpdateForm.bonus_points)
async def incoret_bonus_pointer(message: Message, state: FSMContext) -> None:
    """Если введены некоректные баллы, присутствуют не только числа"""
    await message.answer("Вводим только числа")
    await input_count_bonus(message, state)


async def saly_ouput_data(message, state):
    data = await state.get_data()
    await message.answer(
        f"Установленные пленки: {data.get('films')}\n"
        f"Сумма чека: {data.get('last_cheque')}\n"
        f"Списано баллов: {data.get('bonus_points')}\n\n"
        f"К оплате: {int(data.get('last_cheque')) - data.get('bonus_points')}",
        reply_markup=get_keyboard_sale_save_and_cancel()
    )


@sale_buyer_router.callback_query(F.data == "sale_save")
async def save_obj(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    buyer = await get_object(get_async_session, Buyer, "number", data.get("number"))
    data_buyer = await set_data_buyer_sale(get_async_session, data)
    await update_object(get_async_session, buyer, data_buyer) 
    await callback.message.answer("Продажа проведена 👍", reply_markup=repeat())
    await state.clear()
    await callback.answer()

