import datetime

from typing import Optional

from sqlalchemy.orm import validates
from sqlmodel import SQLModel, Field


class ClientManagerBase(SQLModel):
    first_name: str
    second_name: str
    last_name: str
    phone: str = Field(unique=True, max_length=12)
    email: str = Field(unique=True)

    client_id: Optional[int] = Field(default=None, foreign_key="client.id")


class ClientManager(ClientManagerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    registration_date: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)


class ClientManagerCreate(ClientManagerBase):
    pass


class ClientManagerRead(ClientManagerBase):
    id: int
    registration_date: datetime.datetime


class ClientManagerUpdate(SQLModel):
    first_name: Optional[str]
    second_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str] = Field(unique=True, max_length=12)
    email: Optional[str] = Field(unique=True)

    client_id: Optional[int] = Field(default=None, foreign_key="client.id")
