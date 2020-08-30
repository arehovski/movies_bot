import asyncpg
from main import conn


class DBManager:
    conn: asyncpg.Connection = conn

    async def get_all_movies(self):
        return await self.conn.fetch("SELECT * FROM movies_movie")


db_manager = DBManager()
