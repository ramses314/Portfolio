from typing import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import database_url, sync_database_url

sync_engine = create_engine(sync_database_url, pool_timeout=60)
sync_session_maker = sessionmaker(bind=sync_engine, expire_on_commit=False)

engine = create_async_engine(database_url, pool_timeout=60)
async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


class Base(DeclarativeBase):
    pass


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


def get_sync_session():
    session = sync_session_maker()
    return session
