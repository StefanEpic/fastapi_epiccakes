from typing import List

from fastapi import APIRouter, Depends, Query, UploadFile, File, HTTPException
from fastapi_cache.decorator import cache
from sqlmodel.ext.asyncio.session import AsyncSession

from db.db import get_session
from models.auth import User
from models.store import ImageRead, Product
from repositories.store import ImageRepository
from utils.auth import get_current_user_permissions

router = APIRouter(
    prefix="/images",
    tags=["Images"],
)


@router.get('', response_model=List[ImageRead])
@cache(expire=30)
async def get_list(offset: int = 0, limit: int = Query(default=100, lte=100),
                   session: AsyncSession = Depends(get_session)):
    return await ImageRepository(session).get_list(offset, limit)


@router.get('/{image_id}', response_model=ImageRead)
@cache(expire=30)
async def get_one(image_id: int, session: AsyncSession = Depends(get_session)):
    return await ImageRepository(session).get_one(image_id)


@router.post('', response_model=ImageRead)
async def add_one(product_id: int, image: UploadFile = File(...), session: AsyncSession = Depends(get_session),
                  current_user: User = Depends(get_current_user_permissions)):
    res = await session.get(Product, product_id)
    if not res:
        raise HTTPException(status_code=404, detail="Product with this id not found")
    return await ImageRepository(session).add_one(product_id, image)


@router.delete('/{image_id}')
async def delete_one(image_id: int, session: AsyncSession = Depends(get_session),
                     current_user: User = Depends(get_current_user_permissions)):
    return await ImageRepository(session).delete_one(image_id)
