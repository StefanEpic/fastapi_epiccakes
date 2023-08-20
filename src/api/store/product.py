from typing import List

from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi_cache.decorator import cache
from sqlmodel.ext.asyncio.session import AsyncSession

from db.db import get_session
from models.auth import User
from models.store import ProductCreate, ProductUpdate, Manufacturer, ProductReadWithCategoriesAndImages
from repositories.store import ProductRepository
from utils.auth import get_current_user_permissions

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.get('', response_model=List[ProductReadWithCategoriesAndImages])
@cache(expire=30)
async def get_list(offset: int = 0, limit: int = Query(default=100, lte=100),
                   session: AsyncSession = Depends(get_session)):
    return await ProductRepository(session).get_list(offset, limit)


@router.get('/{product_id}', response_model=ProductReadWithCategoriesAndImages)
@cache(expire=30)
async def get_one(product_id: int, session: AsyncSession = Depends(get_session)):
    return await ProductRepository(session).get_one(product_id)


@router.post('', response_model=ProductReadWithCategoriesAndImages)
async def add_one(product: ProductCreate, session: AsyncSession = Depends(get_session),
                  current_user: User = Depends(get_current_user_permissions)):
    res = await session.get(Manufacturer, product.manufacturer_id)
    if not res:
        raise HTTPException(status_code=404, detail="Manufacturer with this id not found")
    return await ProductRepository(session).add_one(product)


@router.patch('/{product_id}', response_model=ProductReadWithCategoriesAndImages)
async def edit_one(product_id: int, product: ProductUpdate,
                   session: AsyncSession = Depends(get_session),
                   current_user: User = Depends(get_current_user_permissions)):
    if product.manufacturer_id:
        res = await session.get(Manufacturer, product.manufacturer_id)
        if not res:
            raise HTTPException(status_code=404, detail="Manufacturer with this id not found")
    return await ProductRepository(session).edit_one(product_id, product)


@router.delete('/{product_id}')
async def delete_one(product_id: int, session: AsyncSession = Depends(get_session),
                     current_user: User = Depends(get_current_user_permissions)):
    return await ProductRepository(session).delete_one(product_id)
