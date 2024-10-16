import asyncio
from aiogram import Bot, Dispatcher

from config import TOKEN
from app.handlers import router
from app.database.sqlite_db import start_sq
import app.database.sqlite_db as sql


async def main():
    await start_sq()
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router=router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())