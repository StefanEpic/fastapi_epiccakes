import asyncio
from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine
from sqlmodel.ext.asyncio.session import AsyncSession, AsyncEngine

from main import app
from models.store import *
from db.db import get_session

DATABASE_URL_TEST = 'sqlite+aiosqlite:///test.db'

engine_test = AsyncEngine(create_engine(DATABASE_URL_TEST, future=True))
SQLModel.metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


app.dependency_overrides[get_session] = override_get_async_session


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


# SETUP
@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(autouse=True)
async def init_db(ac: AsyncClient):
    await ac.post("/manufacturers", json={
        "title": "ООО Поставщик",
        "city": "Москва",
        "street": "Главная",
        "house": "34",
        "status": "Действующий",
    })

    await ac.post("/manufacturer_managers", json={
        "first_name": "Иван",
        "second_name": "Иванов",
        "last_name": "Иванович",
        "phone": "+79859859898",
        "email": "ivan@test.com",
        "manufacturer_id": 1
    })

    await ac.post("/clients", json={
        "title": "ООО Клиент",
        "city": "Москва",
        "street": "Важная",
        "house": "54",
        "status": "Действующий",
    })

    await ac.post("/client_managers", json={
        "first_name": "Виктор",
        "second_name": "Викторов",
        "last_name": "Викторович",
        "phone": "+78583214589",
        "email": "viktor@test.com",
        "client_id": 1
    })

    await ac.post("/staff_managers", json={
        "first_name": "Борис",
        "second_name": "Борисов",
        "last_name": "Борисович",
        "phone": "+71111111111",
        "email": "boris@test.com",
        "job_title": "Стажер"
    })

    await ac.post("/categories", json={
        "title": "Хит"
    })

    await ac.post("/products", json={
        "title": "Бисквитный пирог",
        "type": "Бисквитные",
        "price": 10,
        "manufacturer_id": 1
    })
