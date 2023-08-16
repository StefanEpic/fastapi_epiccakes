from typing import List

from fastapi import APIRouter, Depends, Query, UploadFile, File, HTTPException
from fastapi_cache.decorator import cache
from sqlmodel import Session

from db.db import get_session
from models.store import ImageRead, Product
from repositories.store import ImageRepository

router = APIRouter(
    prefix="/images",
    tags=["Images"],
)


@router.get('', response_model=List[ImageRead])
@cache(expire=300)
async def get_list(offset: int = 0, limit: int = Query(default=100, lte=100), session: Session = Depends(get_session)):
    return await ImageRepository(session).get_list(offset, limit)


@router.get('/{image_id}', response_model=ImageRead)
@cache(expire=300)
async def get_one(image_id: int, session: Session = Depends(get_session)):
    return await ImageRepository(session).get_one(image_id)


@router.post('', response_model=ImageRead)
async def add_one(product_id: int, image: UploadFile = File(...), session: Session = Depends(get_session)):
    res = await session.get(Product, product_id)
    if not res:
        raise HTTPException(status_code=404, detail="Product with this id not found")
    return await ImageRepository(session).add_one(product_id, image)


@router.delete('/{image_id}')
async def delete_one(image_id: int, session: Session = Depends(get_session)):
    return await ImageRepository(session).delete_one(image_id)
