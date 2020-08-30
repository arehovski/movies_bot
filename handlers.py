import asyncpg
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Command, Text
from main import dp
from database import db_manager


@dp.message_handler(commands=['start'])
async def start_command(message: Message):
    keyboard = ReplyKeyboardMarkup(row_width=2)
    keyboard.add(*(KeyboardButton(text) for text in ('Поиск по названию', 'Фильмы по жанрам', 'Поиск по фильтрам')))
    await message.answer('Привет! Выберите из меню ниже необходимую опцию для поиска нужных фильмов :)',
                        reply_markup=keyboard)


@dp.message_handler(Text('Поиск по названию'))
async def title_search(message: Message):
    await message.answer('Введите название фильма или сериала', reply_markup=ReplyKeyboardMarkup())


