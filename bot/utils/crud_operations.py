from sqlalchemy import select

from db.models import BonusPoint


async def get_object(session, model, attr, param):
    async with session:
        db_obj = await session.execute(
            select(model).filter(getattr(model, attr) == param))
        return db_obj.scalar()
    

async def create_object(session, model, data):
    bonus = await get_object(session, BonusPoint, "name", "bonus_pointer")
    data["count_aplications"] = 1
    data["cheque"] = data.get("last_cheque")
    data["bonus_points"] = (int(data.get("last_cheque")) * bonus.percent) // 100
    obj = model(**data)
    async with session.begin():
        session.add(obj)
    await session.commit()
    print("Добавлен")
        
        