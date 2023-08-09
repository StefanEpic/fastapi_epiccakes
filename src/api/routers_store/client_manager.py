from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session

from db.db import get_session
from models.store import ClientManagerRead, ClientManagerCreate, ClientManagerUpdate
from repositories.store import ClientManagerRepository

router = APIRouter(
    prefix="/client_managers",
    tags=["Client Managers"],
)


@router.get('', response_model=List[ClientManagerRead])
async def get_list(session: Session = Depends(get_session)):
    return await ClientManagerRepository(session).get_list()


@router.get('/{manager_id}', response_model=ClientManagerRead)
async def get_one(manager_id: int, session: Session = Depends(get_session)):
    return await ClientManagerRepository(session).get_one(manager_id)


@router.post('', response_model=ClientManagerRead)
async def add_one(manager: ClientManagerCreate, session: Session = Depends(get_session)):
    return await ClientManagerRepository(session).add_one(manager)


@router.patch('/{manager_id}', response_model=ClientManagerRead)
async def edit_one(manager_id: int, manager: ClientManagerUpdate,
                             session: Session = Depends(get_session)):
    return await ClientManagerRepository(session).edit_one(manager_id, manager)


@router.delete('/{manager_id}')
async def delete_one(manager_id: int, session: Session = Depends(get_session)):
    return await ClientManagerRepository(session).delete_one(manager_id)