from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session

from db.db import get_session
from models.store import ManufacturerManagerRead, ManufacturerManagerCreate, ManufacturerManagerUpdate
from repositories.store import ManufacturerManagerRepository

router = APIRouter(
    prefix="/manufacturer_managers",
    tags=["Manufacturer Managers"],
)


@router.get('', response_model=List[ManufacturerManagerRead])
async def get_list(session: Session = Depends(get_session)):
    return await ManufacturerManagerRepository(session).get_list()


@router.get('/{manager_id}', response_model=ManufacturerManagerRead)
async def get_one(manager_id: int, session: Session = Depends(get_session)):
    return await ManufacturerManagerRepository(session).get_one(manager_id)


@router.post('', response_model=ManufacturerManagerRead)
async def add_one(manager: ManufacturerManagerCreate, session: Session = Depends(get_session)):
    return await ManufacturerManagerRepository(session).add_one(manager)


@router.patch('/{manager_id}', response_model=ManufacturerManagerRead)
async def edit_one(manager_id: int, manager: ManufacturerManagerUpdate,
                             session: Session = Depends(get_session)):
    return await ManufacturerManagerRepository(session).edit_one(manager_id, manager)


@router.delete('/{manager_id}')
async def delete_one(manager_id: int, session: Session = Depends(get_session)):
    return await ManufacturerManagerRepository(session).delete_one(manager_id)
