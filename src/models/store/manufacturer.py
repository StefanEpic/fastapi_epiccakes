import enum
import datetime

from typing import Optional

from sqlmodel import SQLModel, Field


class ManufacturerStatus(enum.Enum):
    active = "Действующий"
    inactive = "Недействующий"


class ManufacturerBase(SQLModel):
    title: str = Field(unique=True)
    description: Optional[str] = Field(default=None)
    city: str
    street: str
    house: str
    office: Optional[str]
    metro_station: Optional[str]
    website: Optional[str]
    status: ManufacturerStatus


class Manufacturer(ManufacturerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    registration_date: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)


class ManufacturerCreate(ManufacturerBase):
    pass


class ManufacturerRead(ManufacturerBase):
    id: int
    registration_date: datetime.datetime


class ManufacturerUpdate(SQLModel):
    title: Optional[str]
    description: Optional[str]
    city: Optional[str]
    street: Optional[str]
    house: Optional[str]
    office: Optional[str]
    metro_station: Optional[str]
    website: Optional[str]
    status: Optional[ManufacturerStatus]
