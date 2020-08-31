import random
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, \
    InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.dispatcher.filters import Command, Text
from main import dp, bot
from database import db_manager


@dp.message_handler(commands=['start'])
async def start_command(message: Message):
    keyboard = ReplyKeyboardMarkup(row_width=2)
    keyboard.add(*(KeyboardButton(text) for text in ('Поиск по названию', 'Поиск по фильтрам', 'Фильмы по жанрам')))
    await message.answer('Привет! Выберите из меню ниже необходимую опцию для поиска нужных фильмов :)',
                        reply_markup=keyboard)


@dp.message_handler(Text('Фильмы по жанрам'))
async def title_search(message: Message):
    keyboard = InlineKeyboardMarkup()
    genres = await db_manager.get_all_genres()
    keyboard.add(*(InlineKeyboardButton(text=genre, callback_data=genre) for genre in genres))
    await message.reply('Выберите жанр', reply_markup=keyboard)


@dp.callback_query_handler() # TODO здесь должны проверяться жанры
async def genre_callback_handler(call: CallbackQuery):
    genre = call.data
    movies = await db_manager.get_movies_from_genre(genre)
    movies = set(random.choices(movies, k=10)) if len(movies) > 10 else movies
    output_msg = '\n'.join(' - '.join((movie.get('title'), str(round(movie.get('rating_kp'), 1)),
                                       f"/{movie.get('movie_id')}")) for movie in movies)
    await call.message.answer(f"Вот несколько случайных фильмов в жанре {genre}:\n{output_msg}")


@dp.message_handler(regexp=r"/\d+")
async def detail_movie_view(message: Message):
    movie_id = message.text[1:]
    movie = await db_manager.get_movie_from_pk(int(movie_id))
    if movie:
        # TODO здесь будет распаковка и представление данных из фильма
        pass
    else:
        await message.answer(f'Сожалеем, фильма с id {movie_id} не существует :(')
