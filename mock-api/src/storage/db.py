from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from core.config import settings


dsn = f'''postgresql+asyncpg://{settings.db_user}:{
    settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}'''
async_engine = create_async_engine(
    dsn, echo=settings.db_debug, future=True)
async_session = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
