from datetime import datetime

from typing import Optional

from sqlmodel import SQLModel, Field


class ManufacturerBase(SQLModel):
    title: str = Field(unique=True)
    description: Optional[str]
    city: str
    street: str
    house: str
    office: Optional[str]
    metro_station: Optional[str]
    website: Optional[str]


class Manufacturer(ManufacturerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # registration_date: datetime = Field(default=datetime.utcnow)


class ManufacturerRead(ManufacturerBase):
    id: int
    # registration_date: datetime


class ManufacturerUpdate(SQLModel):
    title: Optional[str] = Field(unique=True)
    description: Optional[str]
    city: Optional[str]
    street: Optional[str]
    house: Optional[str]
    office: Optional[str]
    metro_station: Optional[str]
    website: Optional[str]
