import datetime
from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, validates

from models.enums import ActiveStatus
from utils.validators import name_valid, phone_valid, email_valid


class Base(DeclarativeBase):
    pass


class AbstractUser(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(50))
    second_name: Mapped[Optional[str]] = mapped_column(String(50))
    last_name: Mapped[Optional[str]] = mapped_column(String(50))
    phone: Mapped[Optional[str]] = mapped_column(String(12), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    registration_date: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow)

    def __str__(self):
        return self.email

    @validates("first_name", "second_name", "last_name")
    def validate_name(self, key, *names):
        for name in names:
            if name:
                return name_valid(name)

    @validates("phone")
    def validate_phone(self, key, phone):
        if phone:
            return phone_valid(phone)

    @validates("email")
    def validate_email(self, key, email):
        return email_valid(email)


class AbstractCompany(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True, index=True)
    description: Mapped[Optional[str]]
    city: Mapped[str] = mapped_column(String(50), index=True)
    street: Mapped[str] = mapped_column(String(50), index=True)
    house: Mapped[str] = mapped_column(String(50))
    office: Mapped[Optional[str]] = mapped_column(String(50))
    metro_station: Mapped[Optional[str]] = mapped_column(String(50), index=True)
    website: Mapped[Optional[str]] = mapped_column(String(50))
    status: Mapped[ActiveStatus] = mapped_column(default=ActiveStatus.active)
    registration_date: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow)

    def __str__(self):
        return self.title
