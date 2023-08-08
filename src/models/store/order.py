import enum
import datetime

from typing import Optional

from sqlalchemy.orm import validates
from sqlmodel import SQLModel, Field


class OrderDelivery(enum.Enum):
    "Доставка" = "delivery"
    "Самовывоз" = "pickup"


class OrderPay(enum.Enum):
    "Наличными" = "cash"
    "Банковской картой" = "card"


class OrderStatus(enum.Enum):
    "В работе" = "processing"
    "Выполнено" = "done"


class OrderBase(SQLModel):
    delivery_method: OrderDelivery
    payment_method: OrderPay
    status: OrderStatus

    client_id: Optional[int] = Field(default=None, foreign_key="client.id")
    staff_manager_id: Optional[int] = Field(default=None, foreign_key="staffmanager.id")
    products: List["Product"] = Relationship(back_populates="orders", link_model=OrderProductLink)


class Order(OrderBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)


class OrderCreate(OrderBase):
    pass


class OrderRead(OrderBase):
    id: int
    date: datetime.datetime


class OrderUpdate(SQLModel):
    delivery_method: Optional[OrderDelivery
    payment_method: Optional[OrderPay
    status: Optional[OrderStatus

    client_id: Optional[int] = Field(default=None, foreign_key="client.id")
    staff_manager_id: Optional[int] = Field(default=None, foreign_key="staffmanager.id")
    products: Optional[List["Product"]] = Relationship(back_populates="orders", link_model=OrderProductLink)
