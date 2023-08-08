import enum

from pydantic import condecimal
from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship

from models.store.category_product_link import CategoryProductLink
from models.store.order_product_link import OrderProductLink


class ProductType(enum.Enum):
    biscuit = "Бисквитные"
    sandy = "Песочные"
    puff = "Слоеные"
    waffle = "Вафельные"
    air = "Воздушные"
    tiny = "Крошковые"
    custards = "Заварные"


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
    # price: condecimal(max_digits=8, decimal_places=2) = Field(default=0)
    price: float

    manufacturer_id: Optional[int] = Field(default=None, foreign_key="manufacturer.id")
    categories: List["Category"] = Relationship(back_populates="products", link_model=CategoryProductLink)
    orders: List["Order"] = Relationship(back_populates="products", link_model=OrderProductLink)


class Product(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: int


class ProductUpdate(SQLModel):
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
    # price: Optional[condecimal]
    price: Optional[float]

    manufacturer_id: Optional[int] = Field(default=None, foreign_key="manufacturer.id")
    categories: Optional[List["Category"]] = Relationship(back_populates="products", link_model=CategoryProductLink)
    orders: Optional[List["Order"]] = Relationship(back_populates="products", link_model=OrderProductLink)
