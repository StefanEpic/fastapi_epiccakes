from typing import Optional

from sqlalchemy.orm import validates
from sqlmodel import SQLModel, Field


class ImageBase(SQLModel):
    title: str
    data: str
    url: str

    product_id: Optional[int] = Field(default=None, foreign_key="product.id")


class Image(ImageBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class ImageCreate(ImageBase):
    pass


class ImageRead(ImageBase):
    id: int


class ImageUpdate(SQLModel):
    title: Optional[str]
    data: Optional[str]
    url: Optional[str]

    product_id: Optional[int] = Field(default=None, foreign_key="product.id")
