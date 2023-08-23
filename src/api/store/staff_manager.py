from typing import List

from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from db.db import get_session
from models.auth import User
from models.store import StaffManagerRead, StaffManagerCreate, StaffManagerUpdate, StaffManagerReadWithOrders
from repositories.store import StaffManagerRepository
from utils.auth import get_current_user_permissions
from utils.depends import Pagination, UserFilter

router = APIRouter(
    prefix="/staff_managers",
    tags=["Staff Managers"],
)


@router.get('', response_model=List[StaffManagerRead])
async def get_list(pagination: Pagination = Depends(Pagination),
                   filters: UserFilter = Depends(UserFilter),
                   session: AsyncSession = Depends(get_session),
                   current_user: User = Depends(get_current_user_permissions)):
    return await StaffManagerRepository(session).get_list(pagination.skip,
                                                          pagination.limit,
                                                          filters.phone,
                                                          filters.email)


@router.get('/{manager_id}', response_model=StaffManagerReadWithOrders)
async def get_one(manager_id: int,
                  session: AsyncSession = Depends(get_session),
                  current_user: User = Depends(get_current_user_permissions)):
    return await StaffManagerRepository(session).get_one(manager_id)


@router.post('', response_model=StaffManagerRead)
async def add_one(manager: StaffManagerCreate,
                  session: AsyncSession = Depends(get_session),
                  current_user: User = Depends(get_current_user_permissions)):
    return await StaffManagerRepository(session).add_one(manager)


@router.patch('/{manager_id}', response_model=StaffManagerRead)
async def edit_one(manager_id: int,
                   manager: StaffManagerUpdate,
                   session: AsyncSession = Depends(get_session),
                   current_user: User = Depends(get_current_user_permissions)):
    return await StaffManagerRepository(session).edit_one(manager_id, manager)


@router.delete('/{manager_id}')
async def delete_one(manager_id: int,
                     session: AsyncSession = Depends(get_session),
                     current_user: User = Depends(get_current_user_permissions)):
    return await StaffManagerRepository(session).delete_one(manager_id)
