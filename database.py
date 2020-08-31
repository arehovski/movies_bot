import asyncpg
from main import conn


class DBManager:
    conn: asyncpg.Connection = conn
    GENRES = "SELECT genre from movies_genre"
    MOVIES_FROM_GENRE = "SELECT * FROM movies_movie JOIN movies_movie_genre mmg on movies_movie.id = mmg.movie_id " \
                       "JOIN movies_genre mg on mg.id = mmg.genre_id where genre = $1"
    MOVIE_FROM_PK = ["SELECT title, year, duration_min, description, rating_kp, link_kp FROM movies_movie where id = $1",
                     "SELECT mg.genre FROM movies_genre JOIN movies_movie_genre mmg on movies_genre.id = mmg.genre_id "
                     "JOIN movies_genre mg on mg.id = mmg.genre_id WHERE movie_id = $1",
                     "SELECT mc.country FROM movies_country JOIN movies_movie_country mmc on "
                     "movies_country.id = mmc.country_id JOIN movies_country mc on "
                     "mc.id = mmc.country_id where movie_id = $1",
                     "SELECT first_name, last_name FROM movies_director JOIN movies_movie mm "
                     "on movies_director.id = mm.director_id where mm.id = $1",
                     "SELECT ma.first_name, ma.last_name FROM movies_actor JOIN movies_movie_actors mma on "
                     "movies_actor.id = mma.actor_id JOIN movies_actor ma on ma.id = mma.actor_id WHERE movie_id = $1"]

    async def get_all_genres(self):
        genres = await self.conn.fetch(self.GENRES)
        return (item.get('genre') for item in genres)

    async def get_movies_from_genre(self, genre):
        return await self.conn.fetch(self.MOVIES_FROM_GENRE, genre)

    async def get_movie_from_pk(self, pk):
        movie_data = await self.conn.fetch(self.MOVIE_FROM_PK[0], pk)
        genres = await self.conn.fetch(self.MOVIE_FROM_PK[1], pk)
        countries = await self.conn.fetch(self.MOVIE_FROM_PK[2], pk)
        director = await self.conn.fetch(self.MOVIE_FROM_PK[3], pk)
        actor = await self.conn.fetch(self.MOVIE_FROM_PK[4], pk)
        return {
            'movie_data': movie_data,
            'genres': genres,
            'countries': countries,
            'director': director,
            'actors': actor
        }



db_manager = DBManager()
