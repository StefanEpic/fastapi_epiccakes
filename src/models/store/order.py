import enum
import datetime

from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship

from models.store.order_product_link import OrderProductLink


class OrderDelivery(enum.Enum):
    delivery = "Доставка"
    pickup = "Самовывоз"


class OrderPay(enum.Enum):
    cash = "Наличными"
    card = "Банковской картой"


class OrderStatus(enum.Enum):
    processing = "В работе"
    done = "Выполнено"


class OrderBase(SQLModel):
    delivery_method: OrderDelivery
    payment_method: OrderPay
    status: OrderStatus

    client_id: Optional[int] = Field(default=None, foreign_key="client.id")
    staff_id: Optional[int] = Field(default=None, foreign_key="staff.id")
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
    delivery_method: Optional[OrderDelivery]
    payment_method: Optional[OrderPay]
    status: Optional[OrderStatus]

    client_id: Optional[int] = Field(default=None, foreign_key="client.id")
    staff_id: Optional[int] = Field(default=None, foreign_key="staff.id")
    products: Optional[List["Product"]] = Relationship(back_populates="orders", link_model=OrderProductLink)


import datetime
import enum

from typing import Optional

from sqlalchemy.orm import validates
from sqlmodel import SQLModel, Field

from utils.validators import name_valid, phone_valid, email_valid


class JobTitle(enum.Enum):
    intern = "Стажер"
    junior = "Младший специалист"
    middle = "Специалист"
    senior = "Ведущий специалист"


class StaffBase(SQLModel):
    first_name: str
    second_name: str
    last_name: str
    phone: str = Field(unique=True, max_length=12)
    email: str = Field(unique=True)
    job_title: JobTitle

    @validates("first_name", "second_name", "last_name")
    def validate_name(self, key, *names):
        for name in names:
            return name_valid(name)

    @validates("phone")
    def validate_phone(self, key, phone):
        return phone_valid(phone)

    @validates("email")
    def validate_email(self, key, email):
        return email_valid(email)


class Staff(StaffBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    registration_date: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)


class StaffCreate(StaffBase):
    pass


class StaffManagerRead(StaffBase):
    id: int
    registration_date: datetime.datetime


class StaffUpdate(SQLModel):
    first_name: Optional[str]
    second_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str] = Field(unique=True, max_length=12)
    email: Optional[str] = Field(unique=True)
    job_title: Optional[JobTitle]
