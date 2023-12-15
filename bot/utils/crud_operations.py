from sqlalchemy import select

from db.models import BonusPoint


async def get_object(session, model, attr, param):
    db_obj = await session.execute(
        select(model).filter(getattr(model, attr) == param))
    return db_obj.scalar()
    

async def create_object(session, model, data):
    bonus = await get_object(session, BonusPoint, "name", "bonus_pointer")
    data["count_aplications"] = 1
    data["cheque"] = data.get("last_cheque")
    data["bonus_points"] = (int(data.get("last_cheque")) * bonus.percent) // 100
    obj = model(**data)
    session.add(obj)
    await session.commit()


async def update_object(session, model, data):
    obj = await get_object(session, model, 'number', data.get('number'))
    for key, value in data.items():
        setattr(obj, key, value)
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
        
        