import asyncio
from typing import AsyncGenerator

import pytest
import redis
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_cache import FastAPICache
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from main import app
from models.auth import *
from db.db import get_session

from repositories.store import *
from repositories.user import UserRepository
from utils.auth import login_for_access_token
from schemas.auth import UserCreate
from schemas.store import *
from models.base import Base

engine_test = create_async_engine('sqlite+aiosqlite:///test.db')
Base.metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = async_sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


app.dependency_overrides[get_session] = override_get_async_session


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

        async_session = async_sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
        async with async_session() as session:
            category1 = CategoryCreate(title="Хит")
            category2 = CategoryCreate(title="Эксклюзив")
            category3 = CategoryCreate(title="Популярное")
            manufacturer = ManufacturerCreate(
                title="ООО Поставщик",
                city="Москва",
                street="Главная",
                house="34"
            )
            manufacturer_manager = ManufacturerManagerCreate(
                first_name="Иван",
                second_name="Иванов",
                last_name="Иванович",
                phone="+79859859898",
                email="ivan@test.com",
                manufacturer_id=1
            )
            customer1 = CustomerCreate(
                title="ООО Клиент",
                city="Москва",
                street="Важная",
                house="54"
            )
            customer2 = CustomerCreate(
                title="ООО Финанс",
                city="Москва",
                street="Успешная",
                house="32"
            )
            customer_manager = CustomerManagerCreate(
                first_name="Виктор",
                second_name="Викторов",
                last_name="Викторович",
                phone="+78583214589",
                email="viktor@test.com",
                customer_id=1
            )
            staff_manager = StaffManagerCreate(
                first_name="Борис",
                second_name="Борисов",
                last_name="Борисович",
                phone="+71111111111",
                email="boris@test.com",
                job_title="Стажер"
            )
            product1 = ProductCreate(
                title="Бисквитный пирог",
                type="Бисквитные",
                price=10,
                manufacturer_id=1,
                categories=[1, 2]
            )
            product2 = ProductCreate(
                title="Клубничный кекс",
                type="Бисквитные",
                price=15,
                manufacturer_id=1,
                categories=[1, 2, 3]
            )
            order = OrderCreate(
                delivery_method="Доставка",
                payment_method="Наличными",
                staff_manager_id=1,
                customer_id=1,
                products={"1": 3, "2": 1}
            )
            review = ReviewCreate(
                rating=5,
                text="Отлично!",
                order_id=1,
                customer_id=1
            )
            user = UserCreate(
                email="admin@admin.com",
                password="12345"
            )
            permission = Permission(title='moderation')

            await CategoryRepository(session).add_one(category1)
            await CategoryRepository(session).add_one(category2)
            await CategoryRepository(session).add_one(category3)
            await ManufacturerRepository(session).add_one(manufacturer)
            await ManufacturerManagerRepository(session).add_one(manufacturer_manager)
            await CustomerRepository(session).add_one(customer1)
            await CustomerRepository(session).add_one(customer2)
            await CustomerManagerRepository(session).add_one(customer_manager)
            await StaffManagerRepository(session).add_one(staff_manager)
            await ProductRepository(session).add_one_product(product1)
            await ProductRepository(session).add_one_product(product2)
            await OrderRepository(session).add_one_order(order)
            await ReviewRepository(session).add_one(review)
            await UserRepository(session).add_one_user(user)

            session.add(permission)
            await session.commit()
            await session.execute(permission_user.insert().values(permission_id=1, user_id=1))
            await session.commit()

    yield

    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


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


async def get_token():
    async_session = async_sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        form_data = OAuth2PasswordRequestForm(username="admin@admin.com", password="12345")
        return await login_for_access_token(form_data, session)


@pytest.fixture(scope="session")
async def auth_ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as auth_ac:
        token = await get_token()
        auth_headers = {"Authorization": f"Bearer {token['access_token']}"}
        auth_ac.headers.update(auth_headers)
        yield auth_ac


@pytest.fixture(scope="session", autouse=True)
def cache_init():
    redis_client = redis.Redis(host='localhost', port=6379)
    FastAPICache.init(backend=redis_client)
