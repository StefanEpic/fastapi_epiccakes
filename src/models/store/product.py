import enum

from pydantic import condecimal
from typing import Optional

from sqlalchemy.orm import validates
from sqlmodel import SQLModel, Field


class ProductType(enum.Enum):
    "Бисквитные" = "biscuit"
    "Песочные" = "sandy"
    "Слоеные" = "puff"
    "Вафельные" = "waffle"
    "Воздушные" = "air"
    "Крошковые" = "tiny"
    "Заварные" = "custards"


class ProductBase(SQLModel):
    title: str = Field(unique=True)
    type: ProductType
    weight: Optional[int]
    best_before_date: Optional[int]
    storage_temperature: Optional[int]
    proteins: Optional[int]
    fats: Optional[int]
    carbohydrates: Optional[int]
    energy_value: Optional[int]
    description: Optional[str]
    price: condecimal(max_digits=8, decimal_places=2) = Field(default=0)

    manufacturer_id: Optional[int] = Field(default=None, foreign_key="manufacturer.id")
    categories: List["Category"] = Relationship(back_populates="products", link_model=CategoryProductLink)
    orders: List["Order"] = Relationship(back_populates="products", link_model=OrderProductLink)


class Product(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: int


classProductUpdate(SQLModel):
    title: Optional[str] = Field(unique=True)
    type: Optional[ProductType]
    weight: Optional[int]
    best_before_date: Optional[int]
    storage_temperature: Optional[int]
    proteins: Optional[int]
    fats: Optional[int]
    carbohydrates: Optional[int]
    energy_value: Optional[int]
    description: Optional[str]
    price: Optional[condecimal]

    manufacturer_id: Optional[int] = Field(default=None, foreign_key="manufacturer.id")
    categories: Optional[List["Category"]] = Relationship(back_populates="products", link_model=CategoryProductLink)
    orders: Optional[List["Order"]] = Relationship(back_populates="products", link_model=OrderProductLink)
