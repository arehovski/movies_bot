from aiogram import types
from main import dp


@dp.message_handler()
async def echo_message(message: types.Message):
    await message.reply(message.text)
