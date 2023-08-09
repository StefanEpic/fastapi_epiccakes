from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session

from db.db import get_session
from models.store import ProductRead, ProductCreate, ProductUpdate
from repositories.store import ProductRepository

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.get('', response_model=List[ProductRead])
async def get_list(session: Session = Depends(get_session)):
    return await ProductRepository(session).get_list()


@router.get('/{product_id}', response_model=ProductRead)
async def get_one(product_id: int, session: Session = Depends(get_session)):
    return await ProductRepository(session).get_one(product_id)


@router.post('', response_model=ProductRead)
async def add_one(product: ProductCreate, session: Session = Depends(get_session)):
    return await ProductRepository(session).add_one(product)


@router.patch('/{product_id}', response_model=ProductRead)
async def edit_one(product_id: int, product: ProductUpdate,
                             session: Session = Depends(get_session)):
    return await ProductRepository(session).edit_one(product_id, product)


@router.delete('/{product_id}')
async def delete_one(product_id: int, session: Session = Depends(get_session)):
    return await ProductRepository(session).delete_one(product_id)