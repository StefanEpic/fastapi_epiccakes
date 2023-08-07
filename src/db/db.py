from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession, AsyncEngine

from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///sqlite.db"

engine = AsyncEngine(create_engine(DATABASE_URL, future=True))


async def get_session() -> AsyncSession:
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
