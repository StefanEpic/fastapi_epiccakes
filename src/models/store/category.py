from typing import Optional

from sqlalchemy.orm import validates
from sqlmodel import SQLModel, Field


class CategoryBase(SQLModel):
    title: str = Field(unique=True)
    description: Optional[str]

    products: List["Product"] = Relationship(back_populates="categories", link_model=CategoryProductLink)


class Category(CategoryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: int


class CategoryUpdate(SQLModel):
    title: Optional[str] = Field(unique=True)
    description: Optional[str]

    products: Optional[List["Product"]] = Relationship(back_populates="categories", link_model=CategoryProductLink)
