from typing import List

from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi_cache.decorator import cache
from sqlmodel.ext.asyncio.session import AsyncSession

from db.db import get_session
from models.auth import User
from models.store import ManufacturerManagerRead, ManufacturerManagerCreate, ManufacturerManagerUpdate, Manufacturer
from repositories.store import ManufacturerManagerRepository
from utils.auth import get_current_user_permissions

router = APIRouter(
    prefix="/manufacturer_managers",
    tags=["Manufacturer Managers"],
)


@router.get('', response_model=List[ManufacturerManagerRead])
@cache(expire=30)
async def get_list(offset: int = 0, limit: int = Query(default=100, lte=100),
                   session: AsyncSession = Depends(get_session),
                   current_user: User = Depends(get_current_user_permissions)):
    return await ManufacturerManagerRepository(session).get_list(offset, limit)


@router.get('/{manager_id}', response_model=ManufacturerManagerRead)
@cache(expire=30)
async def get_one(manager_id: int, session: AsyncSession = Depends(get_session),
                  current_user: User = Depends(get_current_user_permissions)):
    return await ManufacturerManagerRepository(session).get_one(manager_id)


@router.post('', response_model=ManufacturerManagerRead)
async def add_one(manager: ManufacturerManagerCreate, session: AsyncSession = Depends(get_session),
                  current_user: User = Depends(get_current_user_permissions)):
    res = await session.get(Manufacturer, manager.manufacturer_id)
    if not res:
        raise HTTPException(status_code=404, detail="Manufacturer with this id not found")
    return await ManufacturerManagerRepository(session).add_one(manager)


@router.patch('/{manager_id}', response_model=ManufacturerManagerRead)
async def edit_one(manager_id: int, manager: ManufacturerManagerUpdate,
                   session: AsyncSession = Depends(get_session),
                   current_user: User = Depends(get_current_user_permissions)):
    if manager.manufacturer_id:
        res = await session.get(Manufacturer, manager.manufacturer_id)
        if not res:
            raise HTTPException(status_code=404, detail="Manufacturer with this id not found")
    return await ManufacturerManagerRepository(session).edit_one(manager_id, manager)


@router.delete('/{manager_id}')
async def delete_one(manager_id: int, session: AsyncSession = Depends(get_session),
                     current_user: User = Depends(get_current_user_permissions)):
    return await ManufacturerManagerRepository(session).delete_one(manager_id)
