from typing import List

from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi_cache.decorator import cache
from sqlmodel import Session

from db.db import get_session
from models.store import CustomerManagerRead, CustomerManagerCreate, CustomerManagerUpdate, Customer
from repositories.store import CustomerManagerRepository

router = APIRouter(
    prefix="/customer_managers",
    tags=["Customer Managers"],
)


@router.get('', response_model=List[CustomerManagerRead])
@cache(expire=300)
async def get_list(offset: int = 0, limit: int = Query(default=100, lte=100), session: Session = Depends(get_session)):
    return await CustomerManagerRepository(session).get_list(offset, limit)


@router.get('/{manager_id}', response_model=CustomerManagerRead)
@cache(expire=300)
async def get_one(manager_id: int, session: Session = Depends(get_session)):
    return await CustomerManagerRepository(session).get_one(manager_id)


@router.post('', response_model=CustomerManagerRead)
async def add_one(manager: CustomerManagerCreate, session: Session = Depends(get_session)):
    res = await session.get(Customer, manager.customer_id)
    if not res:
        raise HTTPException(status_code=404, detail="Customer with this id not found")
    return await CustomerManagerRepository(session).add_one(manager)


@router.patch('/{manager_id}', response_model=CustomerManagerRead)
async def edit_one(manager_id: int, manager: CustomerManagerUpdate,
                   session: Session = Depends(get_session)):
    if manager.customer_id:
        res = await session.get(Customer, manager.customer_id)
        if not res:
            raise HTTPException(status_code=404, detail="Customer with this id not found")
    return await CustomerManagerRepository(session).edit_one(manager_id, manager)


@router.delete('/{manager_id}')
async def delete_one(manager_id: int, session: Session = Depends(get_session)):
    return await CustomerManagerRepository(session).delete_one(manager_id)
