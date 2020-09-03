import asyncpg
from main import conn


class DBManager:
    conn: asyncpg.Connection = conn
    GENRES = "SELECT genre from movies_genre"
    COUNTRIES = "SELECT country from movies_country"
    MOVIES_FROM_TITLE = "SELECT id, title, rating_kp from movies_movie where to_tsvector(title) @@ " \
                        "plainto_tsquery($1) ORDER BY ts_rank(to_tsvector(title), plainto_tsquery($1)) DESC"
    MOVIES_FROM_GENRE = "SELECT mm.id, title, rating_kp  FROM movies_movie mm JOIN movies_movie_genre mmg " \
                        "on mm.id = mmg.movie_id JOIN movies_genre mg on mg.id = mmg.genre_id where mg.genre = $1"
    MOVIE_FROM_PK = ["SELECT title, year, duration_min, description, rating_kp, link_kp FROM movies_movie where id = $1",
                     "SELECT mg.genre FROM movies_genre mg JOIN movies_movie_genre mmg on mg.id = mmg.genre_id "
                     "WHERE mmg.movie_id = $1",
                     "SELECT mc.country FROM movies_country mc JOIN movies_movie_country mmc on mc.id = mmc.country_id "
                     "where mmc.movie_id = $1",
                     "SELECT md.first_name, md.last_name FROM movies_director md JOIN movies_movie mm "
                     "on md.id = mm.director_id where mm.id = $1",
                     "SELECT ma.first_name, ma.last_name FROM movies_actor ma JOIN movies_movie_actors mma "
                     "on ma.id = mma.actor_id WHERE mma.movie_id = $1"]

    async def get_all_genres(self):
        genres = await self.conn.fetch(self.GENRES)
        return [item.get('genre') for item in genres]

    async def get_all_countries(self):
        countries = await self.conn.fetch(self.COUNTRIES)
        return sorted([item.get('country') for item in countries])

    async def get_movies_from_genre(self, genre):
        return await self.conn.fetch(self.MOVIES_FROM_GENRE, genre)

    async def get_movies_from_title(self, query):
        return await self.conn.fetch(self.MOVIES_FROM_TITLE, query)

    async def get_movie_from_pk(self, pk):
        movie_data, genres, countries, director, actors = \
            [await self.conn.fetch(query, pk) for query in self.MOVIE_FROM_PK]
        return {
            'movie_data': movie_data,
            'genres': genres,
            'countries': countries,
            'director': director,
            'actors': actors
        }


db_manager = DBManager()
