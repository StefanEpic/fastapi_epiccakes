import datetime

from typing import Optional

from sqlalchemy.orm import validates
from sqlmodel import SQLModel, Field

from utils.validators import name_valid, phone_valid, email_valid


class ManufacturerManagerBase(SQLModel):
    first_name: str
    second_name: str
    last_name: str
    phone: str = Field(unique=True, max_length=12)
    email: str = Field(unique=True)

    manufacturer_id: Optional[int] = Field(default=None, foreign_key="manufacturer.id")

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


class ManufacturerManager(ManufacturerManagerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    registration_date: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)


class ManufacturerManagerCreate(ManufacturerManagerBase):
    pass


class ManufacturerManagerRead(ManufacturerManagerBase):
    id: int
    registration_date: datetime.datetime


class ManufacturerManagerUpdate(SQLModel):
    first_name: Optional[str]
    second_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str] = Field(unique=True, max_length=12)
    email: Optional[str] = Field(unique=True)

    manufacturer_id: Optional[int] = Field(default=None, foreign_key="manufacturer.id")
