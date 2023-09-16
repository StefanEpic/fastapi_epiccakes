from fastapi import Query, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from models.store import Customer, Product, StaffManager, Order, Manufacturer
from schemas.store import CustomerManagerCreate, CustomerManagerUpdate, ManufacturerManagerCreate, \
    ManufacturerManagerUpdate, ProductCreate, ProductUpdate, OrderCreate, OrderUpdate, ReviewCreate


class Pagination:
    def __init__(self, skip: int = 0, limit: int = Query(default=100, lte=100)):
        self.skip = skip
        self.limit = limit


class AddressFilter:
    def __init__(self, city: str = None, street: str = None, metro_station: str = None):
        self.city = city
        self.street = street
        self.metro_station = metro_station


class UserFilter:
    def __init__(self, phone: str = None, email: str = None):
        self.phone = phone
        self.email = email


async def customer_create(manager: CustomerManagerCreate,
                          session: AsyncSession = Depends(get_session)) -> CustomerManagerCreate:
    res = await session.get(Customer, manager.customer_id)
    if not res:
        raise HTTPException(status_code=404, detail="Customer with this id not found")
    return manager


async def customer_update(manager: CustomerManagerUpdate,
                          session: AsyncSession = Depends(get_session)) -> CustomerManagerUpdate:
    if manager.customer_id:
        res = await session.get(Customer, manager.customer_id)
        if not res:
            raise HTTPException(status_code=404, detail="Customer with this id not found")
    return manager


async def manufacturer_create(manager: ManufacturerManagerCreate,
                              session: AsyncSession = Depends(get_session)) -> ManufacturerManagerCreate:
    res = await session.get(Manufacturer, manager.manufacturer_id)
    if not res:
        raise HTTPException(status_code=404, detail="Manufacturer with this id not found")
    return manager


async def manufacturer_update(manager: ManufacturerManagerUpdate,
                              session: AsyncSession = Depends(get_session)) -> ManufacturerManagerUpdate:
    if manager.manufacturer_id:
        res = await session.get(Manufacturer, manager.manufacturer_id)
        if not res:
            raise HTTPException(status_code=404, detail="Manufacturer with this id not found")
    return manager


async def product_valid(product_id: int, session: AsyncSession = Depends(get_session)) -> int:
    res = await session.get(Product, product_id)
    if not res:
        raise HTTPException(status_code=404, detail="Product with this id not found")
    return product_id


async def product_create(product: ProductCreate, session: AsyncSession = Depends(get_session)) -> ProductCreate:
    res = await session.get(Manufacturer, product.manufacturer_id)
    if not res:
        raise HTTPException(status_code=404, detail="Manufacturer with this id not found")
    return product


async def product_update(product: ProductUpdate, session: AsyncSession = Depends(get_session)) -> ProductUpdate:
    if product.manufacturer_id:
        res = await session.get(Manufacturer, product.manufacturer_id)
        if not res:
            raise HTTPException(status_code=404, detail="Manufacturer with this id not found")
    return product


async def order_create(order: OrderCreate, session: AsyncSession = Depends(get_session)) -> OrderCreate:
    res_staff = await session.get(StaffManager, order.staff_manager_id)
    if not res_staff:
        raise HTTPException(status_code=404, detail="Staff manager with this id not found")

    res_customer = await session.get(Customer, order.customer_id)
    if not res_customer:
        raise HTTPException(status_code=404, detail="Customer with this id not found")
    return order


async def order_update(order: OrderUpdate, session: AsyncSession = Depends(get_session)) -> OrderUpdate:
    if order.staff_manager_id:
        res_staff = await session.get(StaffManager, order.staff_manager_id)
        if not res_staff:
            raise HTTPException(status_code=404, detail="Staff manager with this id not found")

    if order.customer_id:
        res_customer = await session.get(Customer, order.customer_id)
        if not res_customer:
            raise HTTPException(status_code=404, detail="Customer with this id not found")
    return order


async def review_create(review: ReviewCreate, session: AsyncSession = Depends(get_session)) -> ReviewCreate:
    res_order = await session.get(Order, review.order_id)
    if not res_order:
        raise HTTPException(status_code=404, detail="Order with this id not found")

    res_customer = await session.get(Customer, review.customer_id)
    if not res_customer:
        raise HTTPException(status_code=404, detail="Customer with this id not found")

    if res_order.customer_id != review.customer_id:
        raise HTTPException(status_code=404, detail="This order has a different id customer")
    return review
