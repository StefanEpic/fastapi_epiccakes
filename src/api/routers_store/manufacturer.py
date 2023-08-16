from typing import List

from fastapi import APIRouter, Depends, Query
from fastapi_cache.decorator import cache
from sqlmodel import Session

from db.db import get_session
from models.store import ManufacturerRead, ManufacturerCreate, ManufacturerUpdate, ManufacturerReadWithManagers
from repositories.store import ManufacturerRepository

router = APIRouter(
    prefix="/manufacturers",
    tags=["Manufacturers"],
)


@router.get('', response_model=List[ManufacturerRead])
@cache(expire=300)
async def get_list(offset: int = 0, limit: int = Query(default=100, lte=100), session: Session = Depends(get_session)):
    return await ManufacturerRepository(session).get_list(offset, limit)


@router.get('/{manufacturer_id}', response_model=ManufacturerReadWithManagers)
@cache(expire=300)
async def get_one(manufacturer_id: int, session: Session = Depends(get_session)):
    return await ManufacturerRepository(session).get_one(manufacturer_id)


@router.post('', response_model=ManufacturerRead)
async def add_one(manufacturer: ManufacturerCreate, session: Session = Depends(get_session)):
    return await ManufacturerRepository(session).add_one(manufacturer)


@router.patch('/{manufacturer_id}', response_model=ManufacturerRead)
async def edit_one(manufacturer_id: int, manufacturer: ManufacturerUpdate,
                   session: Session = Depends(get_session)):
    return await ManufacturerRepository(session).edit_one(manufacturer_id, manufacturer)


@router.delete('/{manufacturer_id}')
async def delete_one(manufacturer_id: int, session: Session = Depends(get_session)):
    return await ManufacturerRepository(session).delete_one(manufacturer_id)
