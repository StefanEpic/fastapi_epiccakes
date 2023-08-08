import datetime

from typing import Optional

from sqlmodel import SQLModel, Field


class ReviewBase(SQLModel):
    rating: int = Field(default=0)
    text: str

    client_id: Optional[int] = Field(default=None, foreign_key="client.id")
    order_id: Optional[int] = Field(default=None, foreign_key="order.id")


class Review(ReviewBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date_in: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)


class ReviewCreate(ReviewBase):
    pass


class ReviewRead(ReviewBase):
    id: int
    date_in: datetime.datetime


class ReviewUpdate(SQLModel):
    rating: Optional[int] = Field(default=0)
    text: Optional[str]

    client_id: Optional[int] = Field(default=None, foreign_key="client.id")
    order_id: Optional[int] = Field(default=None, foreign_key="order.id")
