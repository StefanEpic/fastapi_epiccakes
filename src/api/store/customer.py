from typing import List

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlmodel.ext.asyncio.session import AsyncSession

from db.db import get_session
from models.auth import User
from models.store import CustomerRead, CustomerCreate, CustomerUpdate, CustomerReadWithManagers
from repositories.store import CustomerRepository
from utils.auth import get_current_user_permissions
from utils.depends import Pagination, AddressFilter

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


@router.get('', response_model=List[CustomerRead])
@cache(expire=30)
async def get_address_filter_list(pagination: Pagination = Depends(Pagination),
                                  filters: AddressFilter = Depends(AddressFilter),
                                  session: AsyncSession = Depends(get_session),
                                  current_user: User = Depends(get_current_user_permissions)):
    return await CustomerRepository(session).get_address_filter_list(pagination.skip,
                                                                     pagination.limit,
                                                                     filters.city,
                                                                     filters.street,
                                                                     filters.metro_station)


@router.get('/{customer_id}', response_model=CustomerReadWithManagers)
@cache(expire=30)
async def get_one(customer_id: int,
                  session: AsyncSession = Depends(get_session),
                  current_user: User = Depends(get_current_user_permissions)):
    return await CustomerRepository(session).get_one(customer_id)


@router.post('', response_model=CustomerRead)
async def add_one(customer: CustomerCreate,
                  session: AsyncSession = Depends(get_session),
                  current_user: User = Depends(get_current_user_permissions)):
    return await CustomerRepository(session).add_one(customer)


@router.patch('/{customer_id}', response_model=CustomerRead)
async def edit_one(customer_id: int,
                   customer: CustomerUpdate,
                   session: AsyncSession = Depends(get_session),
                   current_user: User = Depends(get_current_user_permissions)):
    return await CustomerRepository(session).edit_one(customer_id, customer)


@router.delete('/{customer_id}')
async def delete_one(customer_id: int,
                     session: AsyncSession = Depends(get_session),
                     current_user: User = Depends(get_current_user_permissions)):
    return await CustomerRepository(session).delete_one(customer_id)
