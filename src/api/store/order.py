from typing import List

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlmodel.ext.asyncio.session import AsyncSession

from db.db import get_session
from models.auth import User
from models.store import OrderRead, OrderCreate, OrderUpdate, OrderReadWithProducts
from repositories.store import OrderRepository
from utils.auth import get_current_user_permissions
from utils.depends import Pagination, order_create, order_update

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


@router.get('', response_model=List[OrderRead])
@cache(expire=30)
async def get_list(pagination: Pagination = Depends(Pagination),
                   session: AsyncSession = Depends(get_session),
                   current_user: User = Depends(get_current_user_permissions)):
    return await OrderRepository(session).get_list(pagination.skip, pagination.limit)


@router.get('/{order_id}', response_model=OrderReadWithProducts)
@cache(expire=30)
async def get_one(order_id: int,
                  session: AsyncSession = Depends(get_session),
                  current_user: User = Depends(get_current_user_permissions)):
    return await OrderRepository(session).get_one(order_id)


@router.post('', response_model=OrderRead)
async def add_one(order: OrderCreate = Depends(order_create),
                  session: AsyncSession = Depends(get_session),
                  current_user: User = Depends(get_current_user_permissions)):
    return await OrderRepository(session).add_one_order(order)


@router.patch('/{order_id}', response_model=OrderReadWithProducts)
async def edit_one(order_id: int,
                   order: OrderUpdate = Depends(order_update),
                   session: AsyncSession = Depends(get_session),
                   current_user: User = Depends(get_current_user_permissions)):
    return await OrderRepository(session).edit_one_order(order_id, order)


@router.delete('/{order_id}')
async def delete_one(order_id: int,
                     session: AsyncSession = Depends(get_session),
                     current_user: User = Depends(get_current_user_permissions)):
    return await OrderRepository(session).delete_one(order_id)
