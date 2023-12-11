from sqlalchemy import select
from db.engine_db import get_async_session
from utils.crud_operations import get_object
from db.models import BonusPoint

async def on_startup():
    """
    Проверяет наличие объекта бонус в бд,
    если нет, то создает.
    
    используется при запуске бота
    """
    obj = await get_object(get_async_session, BonusPoint, 'name', 'bonus_pointer')
    if not obj:
        obj = BonusPoint(name='bonus_pointer')
        async with get_async_session.begin():
            get_async_session.add(obj)
        await get_async_session.commit()
        print("Бонусы добавлены")