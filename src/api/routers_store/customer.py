from typing import List

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from db.db import get_session
from models.store import CustomerRead, CustomerCreate, CustomerUpdate, CustomerReadWithManagers
from repositories.store import CustomerRepository

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


@router.get('', response_model=List[CustomerRead])
async def get_list(offset: int = 0, limit: int = Query(default=100, lte=100), session: Session = Depends(get_session)):
    return await CustomerRepository(session).get_list(offset, limit)


@router.get('/{customer_id}', response_model=CustomerReadWithManagers)
async def get_one(customer_id: int, session: Session = Depends(get_session)):
    return await CustomerRepository(session).get_one(customer_id)


@router.post('', response_model=CustomerRead)
async def add_one(customer: CustomerCreate, session: Session = Depends(get_session)):
    return await CustomerRepository(session).add_one(customer)


@router.patch('/{customer_id}', response_model=CustomerRead)
async def edit_one(customer_id: int, customer: CustomerUpdate,
                   session: Session = Depends(get_session)):
    return await CustomerRepository(session).edit_one(customer_id, customer)


@router.delete('/{customer_id}')
async def delete_one(customer_id: int, session: Session = Depends(get_session)):
    return await CustomerRepository(session).delete_one(customer_id)
