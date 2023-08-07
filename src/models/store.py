import enum
import datetime

from typing import Optional

from sqlalchemy.orm import validates
from sqlmodel import SQLModel, Field


class ManufacturerStatus(enum.Enum):
    active = "Active"
    inactive = "Inactive"


class ManufacturerBase(SQLModel):
    title: str = Field(unique=True)
    description: Optional[str]
    city: str
    street: str
    house: str
    office: Optional[str]
    metro_station: Optional[str]
    website: Optional[str]
    status: ManufacturerStatus

    @validates("website")
    def validate_website(self, key, website):
        if website and "." not in website:
            raise ValueError("invalid value for website field")
        return website


class Manufacturer(ManufacturerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    registration_date: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)


class ManufacturerCreate(ManufacturerBase):
    pass


class ManufacturerRead(ManufacturerBase):
    id: int
    registration_date: datetime.datetime


class ManufacturerUpdate(SQLModel):
    title: Optional[str] = Field(unique=True)
    description: Optional[str]
    city: Optional[str]
    street: Optional[str]
    house: Optional[str]
    office: Optional[str]
    metro_station: Optional[str]
    website: Optional[str]
    status: Optional[ManufacturerStatus]
