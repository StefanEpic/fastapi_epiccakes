from typing import List

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlmodel.ext.asyncio.session import AsyncSession

from db.db import get_session
from models.auth import User
from models.store import CustomerManagerRead, CustomerManagerCreate, CustomerManagerUpdate
from repositories.store import CustomerManagerRepository
from utils.auth import get_current_user_permissions
from utils.depends import Pagination, customer_create, customer_update, UserFilter

router = APIRouter(
    prefix="/customer_managers",
    tags=["Customer Managers"],
)


@router.get('', response_model=List[CustomerManagerRead])
@cache(expire=30)
async def get_list(pagination: Pagination = Depends(Pagination),
                   filters: UserFilter = Depends(UserFilter),
                   session: AsyncSession = Depends(get_session),
                   current_user: User = Depends(get_current_user_permissions)):
    return await CustomerManagerRepository(session).get_list(pagination.skip,
                                                             pagination.limit,
                                                             filters.phone,
                                                             filters.email)


@router.get('/{manager_id}', response_model=CustomerManagerRead)
@cache(expire=30)
async def get_one(manager_id: int,
                  session: AsyncSession = Depends(get_session),
                  current_user: User = Depends(get_current_user_permissions)):
    return await CustomerManagerRepository(session).get_one(manager_id)


@router.post('', response_model=CustomerManagerRead)
async def add_one(manager: CustomerManagerCreate = Depends(customer_create),
                  session: AsyncSession = Depends(get_session),
                  current_user: User = Depends(get_current_user_permissions)):
    return await CustomerManagerRepository(session).add_one(manager)


@router.patch('/{manager_id}', response_model=CustomerManagerRead)
async def edit_one(manager_id: int,
                   manager: CustomerManagerUpdate = Depends(customer_update),
                   session: AsyncSession = Depends(get_session),
                   current_user: User = Depends(get_current_user_permissions)):
    return await CustomerManagerRepository(session).edit_one(manager_id, manager)


@router.delete('/{manager_id}')
async def delete_one(manager_id: int,
                     session: AsyncSession = Depends(get_session),
                     current_user: User = Depends(get_current_user_permissions)):
    return await CustomerManagerRepository(session).delete_one(manager_id)
