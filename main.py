from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import config
import asyncio
import logging
from database import DatabaseManager

logging.basicConfig(level=logging.INFO)

bot = Bot(config.BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

if __name__ == '__main__':
    from handlers import dp
    loop = asyncio.get_event_loop()
    loop.run_until_complete(DatabaseManager.create_db_connection())
    executor.start_polling(dp)
