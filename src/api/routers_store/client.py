from typing import List

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from db.db import get_session
from models.store import ClientRead, ClientCreate, ClientUpdate, ClientReadWithManagers
from repositories.store import ClientRepository

router = APIRouter(
    prefix="/clients",
    tags=["Clients"],
)


@router.get('', response_model=List[ClientRead])
async def get_list(offset: int = 0, limit: int = Query(default=100, lte=100), session: Session = Depends(get_session)):
    return await ClientRepository(session).get_list(offset, limit)


@router.get('/{client_id}', response_model=ClientReadWithManagers)
async def get_one(client_id: int, session: Session = Depends(get_session)):
    return await ClientRepository(session).get_one(client_id)


@router.post('', response_model=ClientRead)
async def add_one(client: ClientCreate, session: Session = Depends(get_session)):
    return await ClientRepository(session).add_one(client)


@router.patch('/{client_id}', response_model=ClientRead)
async def edit_one(client_id: int, client: ClientUpdate,
                   session: Session = Depends(get_session)):
    return await ClientRepository(session).edit_one(client_id, client)


@router.delete('/{client_id}')
async def delete_one(client_id: int, session: Session = Depends(get_session)):
    return await ClientRepository(session).delete_one(client_id)
