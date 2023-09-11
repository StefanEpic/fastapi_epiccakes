from typing import List

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from models.auth import User
from repositories.store import ProductRepository
from schemas.store import ProductCreate, ProductReadWithCategoriesAndImages, ProductUpdate
from utils.auth import get_current_user_permissions
from utils.depends import Pagination, product_create, product_update

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.get('', response_model=List[ProductReadWithCategoriesAndImages])
@cache(expire=30)
async def get_list(pagination: Pagination = Depends(Pagination),
                   session: AsyncSession = Depends(get_session)):
    return await ProductRepository(session).get_list(pagination.skip, pagination.limit)


@router.get('/{product_id}', response_model=ProductReadWithCategoriesAndImages)
@cache(expire=30)
async def get_one(product_id: int,
                  session: AsyncSession = Depends(get_session)):
    return await ProductRepository(session).get_one(product_id)


@router.post('', response_model=ProductReadWithCategoriesAndImages)
async def add_one(product: ProductCreate = Depends(product_create),
                  session: AsyncSession = Depends(get_session),
                  current_user: User = Depends(get_current_user_permissions)):
    return await ProductRepository(session).add_one_product(product)


@router.patch('/{product_id}', response_model=ProductReadWithCategoriesAndImages)
async def edit_one(product_id: int,
                   product: ProductUpdate = Depends(product_update),
                   session: AsyncSession = Depends(get_session),
                   current_user: User = Depends(get_current_user_permissions)):
    return await ProductRepository(session).edit_one_product(product_id, product)


@router.delete('/{product_id}')
async def delete_one(product_id: int,
                     session: AsyncSession = Depends(get_session),
                     current_user: User = Depends(get_current_user_permissions)):
    return await ProductRepository(session).delete_one(product_id)
