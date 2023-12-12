from aiogram import F, Router
from aiogram.types import Message
from aiogram import Router, types
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from keyboards.keyboards import get_key_cancel, get_keyboard_find_buyer, get_keyboard_not_find_duyer, get_keyboard_save_and_cancel
from db.engine_db import get_async_session
from utils.crud_operations import get_object
from db.models import Buyer
from db.states_group import BuyerForm, BuyerUpdateForm
from utils.crud_operations import create_object


sale_buyer_router = Router()


@sale_buyer_router.callback_query(F.data == "sale")
async def input_films(callback: types.CallbackQuery, state: FSMContext):
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


async def input_bonus(message, state):
    data = await state.get_data()
    buyer = await get_object(get_async_session, Buyer, "number", data.get('number'))
    bonus = buyer.bonus_points
    await message.answer(f"Доступно баллов: {bonus}\nВведи сколько списать от 0 до {bonus}")
    await state.set_state(BuyerUpdateForm.bonus_points)


async def chek_correct_bonus(message, state):
    data = await state.get_data()
    buyer = await get_object(get_async_session, Buyer, "number", data.get('number'))
    bonus = buyer.bonus_points
    if int(message.text) > bonus:
        await message.answer(f"Максимальное количесвто для списания {bonus}")
        await input_bonus(message, state)

@sale_buyer_router.message(BuyerUpdateForm.films)
async def set_film_pointer(message: Message, state: FSMContext) -> None:
    # data = await state.get_data()
    # buyer = await get_object(get_async_session, Buyer, number=data.get('number'))
    # bonus = buyer.bonus_points
    await state.update_data(films=message.text)
    await input_bonus(message, state)
    # await message.answer(f"Доступно баллов: {bonus}\nВведи сколько списать от 0 до {bonus}")
    # await state.set_state(BuyerUpdateForm.bonus_points)


@sale_buyer_router.message(BuyerUpdateForm.bonus_points, F.text.regexp(r"^[0-9]+$"))
async def set_bonus_pointer(message: Message, state: FSMContext) -> None:
    await chek_correct_bonus(message, state)
    await state.update_data(bonus_points=int(message.text))
    data = await state.get_data()
    print(data)

@sale_buyer_router.message(BuyerUpdateForm.bonus_points)
async def incoret_bonus_pointer(message: Message, state: FSMContext) -> None:
    await message.answer("Вводим только числа")
    await input_bonus(message, state)