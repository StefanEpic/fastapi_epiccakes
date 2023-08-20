from typing import List

from fastapi import APIRouter, Depends, Query
from fastapi_cache.decorator import cache
from sqlmodel.ext.asyncio.session import AsyncSession

from db.db import get_session
from models.auth import User
from models.store import ManufacturerRead, ManufacturerCreate, ManufacturerUpdate, ManufacturerReadWithManagers
from repositories.store import ManufacturerRepository
from utils.auth import get_current_user_permissions

router = APIRouter(
    prefix="/manufacturers",
    tags=["Manufacturers"],
)


@router.get('', response_model=List[ManufacturerRead])
@cache(expire=30)
async def get_list(offset: int = 0, limit: int = Query(default=100, lte=100),
                   session: AsyncSession = Depends(get_session),
                   current_user: User = Depends(get_current_user_permissions)):
    return await ManufacturerRepository(session).get_list(offset, limit)


@router.get('/{manufacturer_id}', response_model=ManufacturerReadWithManagers)
@cache(expire=30)
async def get_one(manufacturer_id: int, session: AsyncSession = Depends(get_session),
                  current_user: User = Depends(get_current_user_permissions)):
    return await ManufacturerRepository(session).get_one(manufacturer_id)


@router.post('', response_model=ManufacturerRead)
async def add_one(manufacturer: ManufacturerCreate, session: AsyncSession = Depends(get_session),
                  current_user: User = Depends(get_current_user_permissions)):
    return await ManufacturerRepository(session).add_one(manufacturer)


@router.patch('/{manufacturer_id}', response_model=ManufacturerRead)
async def edit_one(manufacturer_id: int, manufacturer: ManufacturerUpdate,
                   session: AsyncSession = Depends(get_session),
                   current_user: User = Depends(get_current_user_permissions)):
    return await ManufacturerRepository(session).edit_one(manufacturer_id, manufacturer)


@router.delete('/{manufacturer_id}')
async def delete_one(manufacturer_id: int, session: AsyncSession = Depends(get_session)):
    return await ManufacturerRepository(session).delete_one(manufacturer_id)
