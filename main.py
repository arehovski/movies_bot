from aiogram import Bot, Dispatcher, executor, types
import config
import asyncio


loop = asyncio.get_event_loop()
bot = Bot(config.BOT_TOKEN)
dp = Dispatcher(bot, loop)


@dp.message_handler()
async def echo_message(message: types.Message):
    await message.reply(message.text)


if __name__ == '__main__':
    executor.start_polling(dp)
