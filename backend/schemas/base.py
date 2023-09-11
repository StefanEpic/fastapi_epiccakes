import datetime
from typing import Optional

from pydantic import BaseModel

from models.enums import ActiveStatus


class AbstractUserCreate(BaseModel):
    first_name: Optional[str] = None
    second_name: Optional[str] = None
    last_name: Optional[str] = None
    email: str


class AbstractUserRead(BaseModel):
    id: int
    first_name: Optional[str] = None
    second_name: Optional[str] = None
    last_name: Optional[str] = None
    email: str
    registration_date: datetime.datetime


class AbstractUserUpdate(BaseModel):
    first_name: Optional[str] = None
    second_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None


class AbstractCompanyCreate(BaseModel):
    title: str
    description: Optional[str] = None
    city: str
    street: str
    house: str
    office: Optional[str] = None
    metro_station: Optional[str] = None
    website: Optional[str] = None


class AbstractCompanyRead(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    city: str
    street: str
    house: str
    office: Optional[str] = None
    metro_station: Optional[str] = None
    website: Optional[str] = None
    status: ActiveStatus
    registration_date: datetime.datetime


class AbstractCompanyUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    city: Optional[str] = None
    street: Optional[str] = None
    house: Optional[str] = None
    office: Optional[str] = None
    metro_station: Optional[str] = None
    website: Optional[str] = None
    status: Optional[ActiveStatus] = None
