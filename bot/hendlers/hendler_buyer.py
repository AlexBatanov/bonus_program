from aiogram import F, Router
from aiogram.types import Message
from aiogram import Router, types
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext


from db.engine_db import get_async_session
from utils.crud_operations import get_object
from db.models import Buyer
from db.states_group import BuyerForm
from utils.crud_operations import create_object

buyer_router = Router()


@buyer_router.message(CommandStart())
async def start_buyer(message: Message, state: FSMContext) -> None:
    await state.set_state(BuyerForm.number)
    await message.answer(
        "Введи номер клиента в формате: 89271112233",
    )


@buyer_router.message(BuyerForm.number, F.text.regexp(r"\d{11}"))
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(number=message.text)

    obj = await get_object(get_async_session, Buyer, 'number', message.text)
    if obj:
        await message.answer(
            f"Имя: {obj.name}\n"
            f"Дата посещения: {obj.date_aplication}\n"
            f"Доступно бонусов: {obj.bonus_points}\n"
            f"Количество установок: {obj.count_aplications}\n"
            f"Сумма последнего чека: {obj.last_cheque}\n"
        )
    else:
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(
            text="Отменить",
            callback_data="cancel")
        )
        builder.add(types.InlineKeyboardButton(
            text="Добавить",
            callback_data="add")
        )
        await message.answer(f"Клиент не найден, добавить?!", reply_markup=builder.as_markup())


@buyer_router.callback_query(F.data == "cancel")
async def cancel(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Отмена")
    await state.get_data()
    await state.clear()
    await callback.answer()


@buyer_router.callback_query(F.data == "add")
async def input_name(callback: types.CallbackQuery, state: FSMContext):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Отменить",
        callback_data="cancel")
    )
    await callback.message.answer("Введи имя клиента", reply_markup=builder.as_markup())
    await state.set_state(BuyerForm.name)
    await callback.answer()


@buyer_router.message(BuyerForm.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(BuyerForm.films)
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Отменить",
        callback_data="cancel")
    )
    await message.answer(
        f"Введи пленки которые установил по типу: глянец на дисплей, скин кожа",
        reply_markup=builder.as_markup()
    )


@buyer_router.message(BuyerForm.films)
async def process_films(message: Message, state: FSMContext):
    await state.update_data(films=message.text)
    await state.set_state(BuyerForm.last_cheque)
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Отменить",
        callback_data="cancel")
    )
    await message.answer(
        f"Введи общую сумму чека по типу: 1590",
        reply_markup=builder.as_markup()
    )


@buyer_router.message(BuyerForm.last_cheque)
async def process_last_cheque(message: Message, state: FSMContext):
    await state.update_data(last_cheque=message.text)
    await state.set_state(BuyerForm.last_cheque)
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Отменить",
        callback_data="cancel")
    )
    builder.add(types.InlineKeyboardButton(
        text="Сохранить",
        callback_data="add_obj")
    )
    data = await state.get_data()

    await message.answer(
        f"Клиент:\nИмя: {data.get('name')}\nНомер: {data.get('number')}\n"
        f"Установленные пленки: {data.get('films')}\n"
        f"Сумма чека: {data.get('last_cheque')}",
        reply_markup=builder.as_markup()
    )


@buyer_router.callback_query(F.data == "add_obj")
async def save_obj(callback: types.CallbackQuery, state: FSMContext):
    await create_object(get_async_session, Buyer, await state.get_data()) 
    await callback.message.answer("Клиент добавлен 👍")
    await state.get_data()
    await state.clear()
    await callback.answer()
    await start_buyer(callback.message, state)
