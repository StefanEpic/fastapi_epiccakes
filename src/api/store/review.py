from typing import List

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlmodel.ext.asyncio.session import AsyncSession

from db.db import get_session
from models.auth import User
from models.store import ReviewRead, ReviewCreate, ReviewUpdate
from repositories.store import ReviewRepository
from utils.auth import get_current_user_permissions
from utils.depends import Pagination, review_create

router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"],
)


@router.get('', response_model=List[ReviewRead])
@cache(expire=30)
async def get_list(pagination: Pagination = Depends(Pagination),
                   session: AsyncSession = Depends(get_session)):
    return await ReviewRepository(session).get_list(pagination.skip, pagination.limit)


@router.get('/{review_id}', response_model=ReviewRead)
@cache(expire=30)
async def get_one(review_id: int,
                  session: AsyncSession = Depends(get_session)):
    return await ReviewRepository(session).get_one(review_id)


@router.post('', response_model=ReviewRead)
async def add_one(review: ReviewCreate = Depends(review_create),
                  session: AsyncSession = Depends(get_session),
                  current_user: User = Depends(get_current_user_permissions)):
    return await ReviewRepository(session).add_one(review)


@router.patch('/{review_id}', response_model=ReviewRead)
async def edit_one(review_id: int,
                   review: ReviewUpdate,
                   session: AsyncSession = Depends(get_session),
                   current_user: User = Depends(get_current_user_permissions)):
    return await ReviewRepository(session).edit_one(review_id, review)


@router.delete('/{review_id}')
async def delete_one(review_id: int,
                     session: AsyncSession = Depends(get_session),
                     current_user: User = Depends(get_current_user_permissions)):
    return await ReviewRepository(session).delete_one(review_id)
