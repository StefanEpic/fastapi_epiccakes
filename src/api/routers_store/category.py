from typing import List

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from db.db import get_session
from models.store import CategoryRead, CategoryCreate, CategoryUpdate
from repositories.store import CategoryRepository

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


@router.get('', response_model=List[CategoryRead])
async def get_list(offset: int = 0, limit: int = Query(default=100, lte=100), session: Session = Depends(get_session)):
    return await CategoryRepository(session).get_list(offset, limit)


@router.get('/{category_id}', response_model=CategoryRead)
async def get_one(category_id: int, session: Session = Depends(get_session)):
    return await CategoryRepository(session).get_one(category_id)


@router.post('', response_model=CategoryRead)
async def add_one(category: CategoryCreate, session: Session = Depends(get_session)):
    return await CategoryRepository(session).add_one(category)


@router.patch('/{category_id}', response_model=CategoryRead)
async def edit_one(category_id: int, category: CategoryUpdate,
                   session: Session = Depends(get_session)):
    return await CategoryRepository(session).edit_one(category_id, category)


@router.delete('/{category_id}')
async def delete_one(category_id: int, session: Session = Depends(get_session)):
    return await CategoryRepository(session).delete_one(category_id)
