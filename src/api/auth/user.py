from logging import getLogger
from typing import List

from fastapi import APIRouter, Query
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from models.auth import UserCreate, UserRead, User
from repositories.user import UserRepository
from utils.auth import get_current_user_permissions

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

logger = getLogger(__name__)


@router.get('', response_model=List[UserRead])
async def get_list(offset: int = 0, limit: int = Query(default=100, lte=100),
                   session: AsyncSession = Depends(get_session),
                   current_user: User = Depends(get_current_user_permissions)):
    return await UserRepository(session).get_list(offset, limit)


@router.get('/{user_id}', response_model=UserRead)
async def get_one(user_id: int, session: AsyncSession = Depends(get_session),
                  current_user: User = Depends(get_current_user_permissions)):
    return await UserRepository(session).get_one(user_id)


@router.post("", response_model=UserRead)
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    try:
        return await UserRepository(session).add_one(user)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@router.patch('/{user_id}', response_model=UserRead)
async def edit_one(user_id: int, user: UserCreate, session: AsyncSession = Depends(get_session),
                   current_user: User = Depends(get_current_user_permissions)):
    return await UserRepository(session).edit_one(user_id, user)


@router.delete('/{user_id}')
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session),
                      current_user: User = Depends(get_current_user_permissions)):
    return await UserRepository(session).delete_one(user_id)
