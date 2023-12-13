from sqlalchemy import select, update

from db.models import BonusPoint, Buyer


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


async def update_object(session, model, data):
    obj = await get_object(session, model, 'number', data.get('number'))
    # del data['number']
    for key, value in data.items():
        setattr(obj, key, value)
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    # stmt = (
    #     update(model).
    #     where(obj.id == obj.id).
    #     values(data)
    #     # returning(User)
    # )
    # result = await session.execute(stmt)
    # await session.commit()
    obj = await get_object(session, Buyer, 'number', data.get('number'))
    print(obj.films)
        
        