import asyncio
import logging
import sys
from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from hendlers.hendler_buyer import buyer_router
from hendlers.start_and_chek_buyer import start_buyer_router
from hendlers.sale_buyer import sale_buyer_router
from hendlers.warranty_buyer import warranty_router
from hendlers.add_employee import admin_router
from hendlers.banned_employee import banned_employee
from db.engine_db import async_engine
from utils.helpers import on_startup

load_dotenv()

TOKEN = getenv("BOT_TOKEN")
# print(TOKEN.strip())
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


async def main() -> None:
    await async_engine()
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    dp.startup.register(on_startup)
    dp.include_routers(start_buyer_router)
    dp.include_router(buyer_router)
    dp.include_router(sale_buyer_router)
    dp.include_router(warranty_router)
    dp.include_router(admin_router)
    dp.include_router(banned_employee)
    
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot exit')