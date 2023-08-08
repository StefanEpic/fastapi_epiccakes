from typing import Optional

from sqlmodel import SQLModel, Field


class OrderProductLink(SQLModel, table=True):
    order_id: Optional[int] = Field(default=None, foreign_key="order.id", primary_key=True)
    product_id: Optional[int] = Field(default=None, foreign_key="product.id", primary_key=True)
    amount: int
