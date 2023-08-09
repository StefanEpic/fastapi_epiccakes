from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session

from db.db import get_session
from models.store import StaffManagerRead, StaffManagerCreate, StaffManagerUpdate
from repositories.store import StaffManagerRepository

router = APIRouter(
    prefix="/staff_managers",
    tags=["Staff Managers"],
)


@router.get('', response_model=List[StaffManagerRead])
async def get_list(session: Session = Depends(get_session)):
    return await StaffManagerRepository(session).get_list()


@router.get('/{manager_id}', response_model=StaffManagerRead)
async def get_one(manager_id: int, session: Session = Depends(get_session)):
    return await StaffManagerRepository(session).get_one(manager_id)


@router.post('', response_model=StaffManagerRead)
async def add_one(manager: StaffManagerCreate, session: Session = Depends(get_session)):
    return await StaffManagerRepository(session).add_one(manager)


@router.patch('/{manager_id}', response_model=StaffManagerRead)
async def edit_one(manager_id: int, manager: StaffManagerUpdate,
                             session: Session = Depends(get_session)):
    return await StaffManagerRepository(session).edit_one(manager_id, manager)


@router.delete('/{manager_id}')
async def delete_one(manager_id: int, session: Session = Depends(get_session)):
    return await StaffManagerRepository(session).delete_one(manager_id)