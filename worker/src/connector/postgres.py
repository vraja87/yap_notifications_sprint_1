import asyncpg
import backoff
from src.logger import logger


class PostgresConnector:
    """Обёртка для соединения, ради backoff"""
    def __init__(self, dsn):
        """Инициализирует асинхронное соединение с PostgreSQL."""
        self.dsn = dsn
        self.connection = None

    @logger.catch
    @backoff.on_exception(backoff.expo, asyncpg.exceptions.PostgresError, max_tries=3)
    async def connect(self):
        """Асинхронно устанавливает соединение с базой данных."""
        self.connection = await asyncpg.connect(self.dsn)

    @logger.catch
    @backoff.on_exception(backoff.expo, asyncpg.exceptions.PostgresError, max_tries=3)
    async def fetch(self, query, *params):
        """Выполняет SQL запрос с возможными параметрами."""
        return await self.connection.fetch(query, *params)

    async def close(self):
        """Закрывает соединение с базой."""
        if self.connection:
            await self.connection.close()
            logger.info("DB connection closed.")
