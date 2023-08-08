import enum
import datetime

from typing import Optional

from sqlmodel import SQLModel, Field


class ClientStatus(enum.Enum):
    active = "Действующий"
    inactive = "Недействующий"


class ClientBase(SQLModel):
    title: str = Field(unique=True)
    description: Optional[str]
    city: str
    street: str
    house: str
    office: Optional[str]
    metro_station: Optional[str]
    website: Optional[str]
    status: ClientStatus


class Client(ClientBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    registration_date: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)


class ClientCreate(ClientBase):
    pass


class ClientRead(ClientBase):
    id: int
    registration_date: datetime.datetime


class ClientUpdate(SQLModel):
    title: Optional[str] = Field(unique=True)
    description: Optional[str]
    city: Optional[str]
    street: Optional[str]
    house: Optional[str]
    office: Optional[str]
    metro_station: Optional[str]
    website: Optional[str]
    status: Optional[ClientStatus]
