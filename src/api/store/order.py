from typing import List

from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi_cache.decorator import cache
from sqlmodel.ext.asyncio.session import AsyncSession

from db.db import get_session
from models.auth import User
from models.store import OrderRead, OrderCreate, OrderUpdate, OrderReadWithProducts, StaffManager, Customer
from repositories.store import OrderRepository
from utils.auth import get_current_user_permissions

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


@router.get('', response_model=List[OrderRead])
@cache(expire=30)
async def get_list(offset: int = 0, limit: int = Query(default=100, lte=100),
                   session: AsyncSession = Depends(get_session),
                   current_user: User = Depends(get_current_user_permissions)):
    return await OrderRepository(session).get_list(offset, limit)


@router.get('/{order_id}', response_model=OrderReadWithProducts)
@cache(expire=30)
async def get_one(order_id: int, session: AsyncSession = Depends(get_session),
                  current_user: User = Depends(get_current_user_permissions)):
    return await OrderRepository(session).get_one(order_id)


@router.post('', response_model=OrderRead)
async def add_one(order: OrderCreate, session: AsyncSession = Depends(get_session),
                  current_user: User = Depends(get_current_user_permissions)):
    res_staff = await session.get(StaffManager, order.staffmanager_id)
    if not res_staff:
        raise HTTPException(status_code=404, detail="Staff manager with this id not found")

    res_customer = await session.get(Customer, order.customer_id)
    if not res_customer:
        raise HTTPException(status_code=404, detail="Customer with this id not found")
    return await OrderRepository(session).add_one(order)


@router.patch('/{order_id}', response_model=OrderReadWithProducts)
async def edit_one(order_id: int, order: OrderUpdate,
                   session: AsyncSession = Depends(get_session),
                   current_user: User = Depends(get_current_user_permissions)):
    if order.staffmanager_id:
        res_staff = await session.get(StaffManager, order.staffmanager_id)
        if not res_staff:
            raise HTTPException(status_code=404, detail="Staff manager with this id not found")

    if order.customer_id:
        res_customer = await session.get(Customer, order.customer_id)
        if not res_customer:
            raise HTTPException(status_code=404, detail="Customer with this id not found")
    return await OrderRepository(session).edit_one(order_id, order)


@router.delete('/{order_id}')
async def delete_one(order_id: int, session: AsyncSession = Depends(get_session),
                     current_user: User = Depends(get_current_user_permissions)):
    return await OrderRepository(session).delete_one(order_id)
