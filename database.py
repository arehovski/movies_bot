import asyncpg
import config


class DatabaseManager:

    @staticmethod
    async def create_db_connection():
        conn: asyncpg.Connection = await asyncpg.connect(
            database='movies',
            host=config.PG_HOST,
            port=config.PG_PORT,
            user=config.PG_USER,
            password=config.PG_PASS
        )
        users = await conn.execute('SELECT * FROM movies_genre')
        print(users)
