from typing import List

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlmodel.ext.asyncio.session import AsyncSession

from db.db import get_session
from models.auth import User
from models.store import ManufacturerManagerRead, ManufacturerManagerCreate, ManufacturerManagerUpdate
from repositories.store import ManufacturerManagerRepository
from utils.auth import get_current_user_permissions
from utils.depends import Pagination, manufacturer_create, manufacturer_update, UserFilter

router = APIRouter(
    prefix="/manufacturer_managers",
    tags=["Manufacturer Managers"],
)


@router.get('', response_model=List[ManufacturerManagerRead])
@cache(expire=30)
async def get_user_filter_list(pagination: Pagination = Depends(Pagination),
                               filters: UserFilter = Depends(UserFilter),
                               session: AsyncSession = Depends(get_session),
                               current_user: User = Depends(get_current_user_permissions)):
    return await ManufacturerManagerRepository(session).get_user_filter_list(pagination.skip,
                                                                             pagination.limit,
                                                                             filters.phone,
                                                                             filters.email)


@router.get('/{manager_id}', response_model=ManufacturerManagerRead)
@cache(expire=30)
async def get_one(manager_id: int,
                  session: AsyncSession = Depends(get_session),
                  current_user: User = Depends(get_current_user_permissions)):
    return await ManufacturerManagerRepository(session).get_one(manager_id)


@router.post('', response_model=ManufacturerManagerRead)
async def add_one(manager: ManufacturerManagerCreate = Depends(manufacturer_create),
                  session: AsyncSession = Depends(get_session),
                  current_user: User = Depends(get_current_user_permissions)):
    return await ManufacturerManagerRepository(session).add_one(manager)


@router.patch('/{manager_id}', response_model=ManufacturerManagerRead)
async def edit_one(manager_id: int,
                   manager: ManufacturerManagerUpdate = Depends(manufacturer_update),
                   session: AsyncSession = Depends(get_session),
                   current_user: User = Depends(get_current_user_permissions)):
    return await ManufacturerManagerRepository(session).edit_one(manager_id, manager)


@router.delete('/{manager_id}')
async def delete_one(manager_id: int,
                     session: AsyncSession = Depends(get_session),
                     current_user: User = Depends(get_current_user_permissions)):
    return await ManufacturerManagerRepository(session).delete_one(manager_id)
