from typing import List

from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi_cache.decorator import cache
from sqlmodel import Session

from db.db import get_session
from models.store import ReviewRead, ReviewCreate, ReviewUpdate, Order, Customer
from repositories.store import ReviewRepository

router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"],
)


@router.get('', response_model=List[ReviewRead])
@cache(expire=300)
async def get_list(offset: int = 0, limit: int = Query(default=100, lte=100), session: Session = Depends(get_session)):
    return await ReviewRepository(session).get_list(offset, limit)


@router.get('/{review_id}', response_model=ReviewRead)
@cache(expire=300)
async def get_one(review_id: int, session: Session = Depends(get_session)):
    return await ReviewRepository(session).get_one(review_id)


@router.post('', response_model=ReviewRead)
async def add_one(review: ReviewCreate, session: Session = Depends(get_session)):
    res_order = await session.get(Order, review.order_id)
    if not res_order:
        raise HTTPException(status_code=404, detail="Order with this id not found")

    res_customer = await session.get(Customer, review.customer_id)
    if not res_customer:
        raise HTTPException(status_code=404, detail="Customer with this id not found")

    if res_order.customer_id != review.customer_id:
        raise HTTPException(status_code=404, detail="This order has a different id customer")

    return await ReviewRepository(session).add_one(review)


@router.patch('/{review_id}', response_model=ReviewRead)
async def edit_one(review_id: int, review: ReviewUpdate,
                   session: Session = Depends(get_session)):
    return await ReviewRepository(session).edit_one(review_id, review)


@router.delete('/{review_id}')
async def delete_one(review_id: int, session: Session = Depends(get_session)):
    return await ReviewRepository(session).delete_one(review_id)
