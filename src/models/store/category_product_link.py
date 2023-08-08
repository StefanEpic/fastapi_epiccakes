from typing import Optional

from sqlalchemy.orm import validates
from sqlmodel import SQLModel, Field


class CategoryProductLink(SQLModel, table=True):
    category_id: Optional[int] = Field(default=None, foreign_key="category.id", primary_key=True)
    product_id: Optional[int] = Field(default=None, foreign_key="product.id", primary_key=True)
