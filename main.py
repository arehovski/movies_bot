import asyncpg
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import config
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

bot = Bot(config.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())
loop = asyncio.get_event_loop()


async def create_db_connection():
    return await asyncpg.create_pool(
        database='movies',
        host=config.PG_HOST,
        port=config.PG_PORT,
        user=config.PG_USER,
        password=config.PG_PASS
    )


conn = loop.run_until_complete(create_db_connection())

if __name__ == '__main__':
    from handlers import dp
    executor.start_polling(dp)
