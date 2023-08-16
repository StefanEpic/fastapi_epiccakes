from typing import List

from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi_cache.decorator import cache
from sqlmodel import Session

from db.db import get_session
from models.store import ProductCreate, ProductUpdate, Manufacturer, ProductReadWithCategoriesAndImages
from repositories.store import ProductRepository

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.get('', response_model=List[ProductReadWithCategoriesAndImages])
@cache(expire=300)
async def get_list(offset: int = 0, limit: int = Query(default=100, lte=100), session: Session = Depends(get_session)):
    return await ProductRepository(session).get_list(offset, limit)


@router.get('/{product_id}', response_model=ProductReadWithCategoriesAndImages)
@cache(expire=300)
async def get_one(product_id: int, session: Session = Depends(get_session)):
    return await ProductRepository(session).get_one(product_id)


@router.post('', response_model=ProductReadWithCategoriesAndImages)
async def add_one(product: ProductCreate, session: Session = Depends(get_session)):
    res = await session.get(Manufacturer, product.manufacturer_id)
    if not res:
        raise HTTPException(status_code=404, detail="Manufacturer with this id not found")
    return await ProductRepository(session).add_one(product)


@router.patch('/{product_id}', response_model=ProductReadWithCategoriesAndImages)
async def edit_one(product_id: int, product: ProductUpdate,
                   session: Session = Depends(get_session)):
    if product.manufacturer_id:
        res = await session.get(Manufacturer, product.manufacturer_id)
        if not res:
            raise HTTPException(status_code=404, detail="Manufacturer with this id not found")
    return await ProductRepository(session).edit_one(product_id, product)


@router.delete('/{product_id}')
async def delete_one(product_id: int, session: Session = Depends(get_session)):
    return await ProductRepository(session).delete_one(product_id)
