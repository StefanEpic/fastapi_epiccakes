import datetime

from typing import Optional

from sqlalchemy.orm import validates
from sqlmodel import SQLModel, Field


class JobTitle(enum.Enum):
    "Стажер" = "intern"
    "Младший специалист" = "junior"
    "Специалист" = "middle"
    "Ведущий специалист" = "senior"


class StaffManagerBase(SQLModel):
    first_name: str
    second_name: str
    last_name: str
    phone: str = Field(unique=True, max_length=12)
    email: str = Field(unique=True)
    job_title: JobTitle


class StaffManager(StaffManagerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    registration_date: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)


class StaffManagerCreate(StaffManagerBase):
    pass


class StaffManagerRead(StaffManagerBase):
    id: int
    registration_date: datetime.datetime


class StaffManagerUpdate(SQLModel):
    first_name: Optional[str]
    second_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str] = Field(unique=True, max_length=12)
    email: Optional[str] = Field(unique=True)
    job_title: Optional[JobTitle]
