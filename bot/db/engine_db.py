from os import getenv
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from .models import Base


load_dotenv()

engine = create_async_engine(getenv("DB_URL"), echo=True)
# async_session = async_sessionmaker(engine)

Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
get_async_session = Session()

async def async_engine():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)