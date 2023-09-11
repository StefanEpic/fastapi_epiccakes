from typing import List, Optional

from pydantic import BaseModel

from schemas.base import AbstractUserCreate, AbstractUserRead, AbstractUserUpdate


class PermissionCreate(BaseModel):
    title: str


class PermissionRead(BaseModel):
    id: int
    title: str


class PermissionUpdate(BaseModel):
    title: str


class UserCreate(AbstractUserCreate):
    password: str
    phone: Optional[str] = None


class UserRead(AbstractUserRead):
    phone: Optional[str] = None
    is_active: bool
    permissions: List["PermissionRead"]


class UserUpdate(AbstractUserUpdate):
    phone: Optional[str] = None
    password: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str
