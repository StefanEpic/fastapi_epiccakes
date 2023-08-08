from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session

from db.db import get_session
from models.store.manufacturer import ManufacturerRead, ManufacturerCreate, ManufacturerUpdate
from repositories.store import ManufacturerRepository

router = APIRouter(
    prefix="/manufacturers",
    tags=["Manufacturer"],
)


@router.get('', response_model=List[ManufacturerRead])
async def get_manufacturers(session: Session = Depends(get_session)):
    return await ManufacturerRepository(session).get_list()


@router.get('/{manufacturer_id}', response_model=ManufacturerRead)
async def get_manufacturer(manufacturer_id: int, session: Session = Depends(get_session)):
    return await ManufacturerRepository(session).get_one(manufacturer_id)


@router.post('', response_model=ManufacturerRead)
async def add_manufacturer(manufacturer: ManufacturerCreate, session: Session = Depends(get_session)):
    return await ManufacturerRepository(session).add_one(manufacturer)


@router.patch('/{manufacturer_id}', response_model=ManufacturerRead)
async def patch_manufacturer(manufacturer_id: int, manufacturer: ManufacturerUpdate,
                             session: Session = Depends(get_session)):
    return await ManufacturerRepository(session).edit_one(manufacturer_id, manufacturer)


@router.delete('/{manufacturer_id}')
async def patch_manufacturer(manufacturer_id: int, session: Session = Depends(get_session)):
    return await ManufacturerRepository(session).delete_one(manufacturer_id)
