import random
from datetime import datetime
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, \
    InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from main import dp, bot
from database import db_manager


genres = None


def movies_output_message(movies):
    return '\n'.join(' - '.join((movie.get('title'), str(round(movie.get('rating_kp'), 1)),
                                 f"/{movie.get('id')}")) for movie in movies)


class FiltersSearchState(StatesGroup):
    genre_state = State('genre')
    country_state = State('country')
    year_state = State('year')


@dp.message_handler(commands=['start'])
async def start_command(message: Message):
    keyboard = ReplyKeyboardMarkup(row_width=2)
    keyboard.add(*(KeyboardButton(text) for text in ('Поиск по названию', 'Поиск по фильтрам', 'Фильмы по жанрам')))
    await message.answer('Привет! Выберите из меню ниже необходимую опцию для поиска нужных фильмов :)',
                         reply_markup=keyboard)


@dp.message_handler(Text('Поиск по названию'))
async def title_search_reply(message: Message):
    await message.reply("<i>Введите название фильма. Например:</i> <b>Побег из Шоушенка.</b>", parse_mode='HTML')


@dp.message_handler(Text('Фильмы по жанрам'))
async def genres_keyboard_reply(message: Message):
    keyboard = InlineKeyboardMarkup()
    global genres
    genres = await db_manager.get_all_genres()
    keyboard.add(*(InlineKeyboardButton(text=genre, callback_data=genre) for genre in genres))
    await message.reply('Выберите жанр', reply_markup=keyboard)


@dp.message_handler(Text('Поиск по фильтрам'))
async def filters_search_reply(message: Message):
    keyboard = ReplyKeyboardMarkup()
    genres = await db_manager.get_all_genres()
    keyboard.add(KeyboardButton('все'))
    keyboard.add(*(KeyboardButton(genre) for genre in genres))
    await message.answer("<i>Выберите жанр</i>", reply_markup=keyboard, parse_mode='HTML')
    await FiltersSearchState.genre_state.set()


@dp.message_handler(state=FiltersSearchState.genre_state)
async def genre_state_reply(message: Message, state: FSMContext):
    genre = message.text
    await state.update_data(genre=genre)
    keyboard = ReplyKeyboardMarkup()
    keyboard.add(KeyboardButton('все'))
    countries = await db_manager.get_all_countries()
    keyboard.add(*(KeyboardButton(country) for country in countries))
    await message.answer("<i>Выберите страну</i>", reply_markup=keyboard, parse_mode='HTML')
    await FiltersSearchState.country_state.set()


@dp.message_handler(state=FiltersSearchState.country_state)
async def country_state_reply(message: Message, state: FSMContext):
    country = message.text
    await state.update_data(country=country)
    keyboard = ReplyKeyboardMarkup()
    keyboard.add(KeyboardButton('все'))
    keyboard.add(*(KeyboardButton(str(year)) for year in range(datetime.now().year, 1920, -1)))
    await message.answer("<i>Выберите год</i>", reply_markup=keyboard, parse_mode='HTML')
    await FiltersSearchState.year_state.set()


@dp.message_handler(state=FiltersSearchState.year_state)
async def year_state_reply(message: Message, state: FSMContext):
    year = message.text
    country = state.get_data('country')
    genre = state.get_data('genre')
    movies = None # TODO интерсект запрос к базе


@dp.callback_query_handler(lambda call: call.data in genres)
async def random_movies_from_genre(call: CallbackQuery):
    genre = call.data
    movies = await db_manager.get_movies_from_genre(genre)
    movies = set(random.choices(movies, k=10)) if len(movies) > 10 else movies
    output_msg = movies_output_message(movies)
    await call.message.answer(f"Вот несколько случайных фильмов в жанре {genre}:\n{output_msg}")


@dp.message_handler(regexp=r"/\d+")
async def detail_movie_reply(message: Message):
    movie_id = message.text[1:]
    movie = await db_manager.get_movie_from_pk(int(movie_id))
    if movie:
        movie_data = movie.get('movie_data')[0]
        title = movie_data.get('title')
        year = str(movie_data.get('year'))
        duration = str(movie_data.get('duration_min'))
        description = movie_data.get('description')
        rating = str(round(movie_data.get('rating_kp'), 1))
        link_kb = f'http://161.35.201.129/movie/{movie_id}'
        link_kp = movie_data.get('link_kp')
        genres = ', '.join([genre.get('genre') for genre in movie.get('genres')])
        countries = ', '.join([country.get('country') for country in movie.get('countries')])
        director = movie.get('director')[0]
        director = ' '.join((director.get('first_name'), director.get('last_name')))
        actors = ', '.join([' '.join((actor.get('first_name'), actor.get('last_name'))) for actor in movie.get('actors')])
        msg = f"<b>{title}</b>\n<i>Год:</i> {year}\n<i>Длительность:</i> {duration} мин.\n<i>Жанры:</i> {genres}\n" \
              f"<i>Страна:</i> {countries}\n<i>Описание:</i>\n{description}\n<i>Рейтинг кинопоиска</i> - {rating}\n" \
              f"<i>Режиссер:</i> {director}\n<i>В главных ролях:</i> {actors}"
        keyboard = InlineKeyboardMarkup()
        kb_link_button = InlineKeyboardButton("Kinobar", url=link_kb)
        kp_link_button = InlineKeyboardButton("Kinopoisk", url=link_kp)
        keyboard.add(kp_link_button, kb_link_button)
        await message.answer(msg, reply_markup=keyboard, parse_mode='HTML')
    else:
        await message.answer(f'Сожалеем, фильма с id {movie_id} не существует :(')


@dp.message_handler(regexp=r"\w+")
async def title_movie_search(message: Message):
    query = message.text
    movies = await db_manager.get_movies_from_title(query)
    if movies:
        output_message = movies_output_message(movies)
        await message.answer(f"Вот что удалось найти по запросу {query}:\n{output_message}")
    else:
        await message.answer(f"К сожалению, по запросу {query} ничего не найдено :(")
