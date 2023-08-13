import os

from sqlmodel import create_engine
from sqlmodel.ext.asyncio.session import AsyncSession, AsyncEngine

from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'sqlite+aiosqlite:///sqlite.db'
SITE_URL = '127.0.0.1:8000'
MEDIA_URL = f'{os.path.abspath(os.curdir)}/media'

engine = AsyncEngine(create_engine(DATABASE_URL, future=True))


async def get_session() -> AsyncSession:
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
