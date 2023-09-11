from typing import List

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from models.auth import User
from repositories.store import CategoryRepository
from schemas.store import CategoryRead, CategoryCreate, CategoryUpdate
from utils.auth import get_current_user_permissions
from utils.depends import Pagination

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


@router.get('', response_model=List[CategoryRead])
@cache(expire=30)
async def get_list(pagination: Pagination = Depends(Pagination),
                   session: AsyncSession = Depends(get_session)):
    return await CategoryRepository(session).get_list(pagination.skip,
                                                      pagination.limit)


@router.get('/{category_id}', response_model=CategoryRead)
@cache(expire=30)
async def get_one(category_id: int,
                  session: AsyncSession = Depends(get_session)):
    return await CategoryRepository(session).get_one(category_id)


@router.post('', response_model=CategoryRead)
async def add_one(category: CategoryCreate,
                  session: AsyncSession = Depends(get_session),
                  current_user: User = Depends(get_current_user_permissions)):
    return await CategoryRepository(session).add_one(category)


@router.patch('/{category_id}', response_model=CategoryRead)
async def edit_one(category_id: int,
                   category: CategoryUpdate,
                   session: AsyncSession = Depends(get_session),
                   current_user: User = Depends(get_current_user_permissions)):
    return await CategoryRepository(session).edit_one(category_id, category)


@router.delete('/{category_id}')
async def delete_one(category_id: int,
                     session: AsyncSession = Depends(get_session),
                     current_user: User = Depends(get_current_user_permissions)):
    return await CategoryRepository(session).delete_one(category_id)
