from datetime import datetime
from sqlalchemy import select
from db.engine_db import get_async_session
from utils.crud_operations import get_object
from db.models import BonusPoint, Buyer


async def on_startup():
    """
    Проверяет наличие объекта бонус в бд,
    если нет, то создает.
    
    используется при запуске бота
    """
    obj = await get_object(get_async_session, BonusPoint, 'name', 'bonus_pointer')
    if not obj:
        obj = BonusPoint(name='bonus_pointer')
        # async with get_async_session.begin():
        get_async_session.add(obj)
        await get_async_session.commit()
        print("Бонусы добавлены")


async def set_data_buyer_sale(session, data):
    """Обновляем словарь для обновления данных о продаже"""

    obj = await get_object(session, Buyer, 'number', data.get('number'))
    bonus = await get_object(get_async_session, BonusPoint, 'name', 'bonus_pointer')
    data["cheque"] = obj.cheque + data.get("last_cheque")
    cur_bonus = data.get("bonus_points")
    data["bonus_points"] = (
        (data.get("last_cheque") - data.get("bonus_points")) * bonus.percent // 100
        ) + obj.bonus_points - data.get("bonus_points")
    data["last_cheque"] -= cur_bonus
    data["count_aplications"] = obj.count_aplications + 1
    data["date_aplication"] = datetime.now()
    return data


async def set_data_buyer_create(session, data):
    bonus = await get_object(session, BonusPoint, "name", "bonus_pointer")
    data["count_aplications"] = 1
    data["cheque"] = data.get("last_cheque")
    data["bonus_points"] = (int(data.get("last_cheque")) * bonus.percent) // 100
    return data