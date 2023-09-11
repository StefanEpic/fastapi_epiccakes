from typing import List

from fastapi import APIRouter, Depends, UploadFile, File
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from models.auth import User
from repositories.store import ImageRepository
from schemas.store import ImageRead
from utils.auth import get_current_user_permissions
from utils.depends import Pagination, product_valid

router = APIRouter(
    prefix="/images",
    tags=["Images"],
)


@router.get('', response_model=List[ImageRead])
@cache(expire=30)
async def get_list(pagination: Pagination = Depends(Pagination),
                   session: AsyncSession = Depends(get_session)):
    return await ImageRepository(session).get_list(pagination.skip, pagination.limit)


@router.get('/{image_id}', response_model=ImageRead)
@cache(expire=30)
async def get_one(image_id: int,
                  session: AsyncSession = Depends(get_session)):
    return await ImageRepository(session).get_one(image_id)


@router.post('', response_model=ImageRead)
async def add_one(product_id: int = Depends(product_valid),
                  image: UploadFile = File(...),
                  session: AsyncSession = Depends(get_session),
                  current_user: User = Depends(get_current_user_permissions)):
    return await ImageRepository(session).add_one_image(product_id, image)


@router.delete('/{image_id}')
async def delete_one(image_id: int,
                     session: AsyncSession = Depends(get_session),
                     current_user: User = Depends(get_current_user_permissions)):
    return await ImageRepository(session).delete_one_image(image_id)
