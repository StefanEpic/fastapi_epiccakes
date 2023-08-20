import datetime

from typing import Optional, List

from sqlalchemy.orm import validates
from sqlmodel import SQLModel, Field, Relationship

from utils.validators import name_valid, phone_valid, email_valid


# ------------------------------
# ----- PermissionUserLink -----
# ------------------------------
class PermissionUserLink(SQLModel, table=True):
    permission_id: Optional[int] = Field(default=None, foreign_key="permission.id", primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True)


# ----------------------
# ----- Permission -----
# ----------------------
class PermissionBase(SQLModel):
    title: str = Field(unique=True)


class Permission(PermissionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    users: List["User"] = Relationship(back_populates="permissions", link_model=PermissionUserLink)

    def __str__(self):
        return self.title


class PermissionCreate(PermissionBase):
    pass


class PermissionRead(PermissionBase):
    pass


class PermissionUpdate(SQLModel):
    title: Optional[str] = Field(unique=True)


# ----------------
# ----- User -----
# ----------------

class UserBase(SQLModel):
    first_name: Optional[str]
    second_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str] = Field(unique=True, max_length=12)
    email: str = Field(unique=True, nullable=False)

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


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    registration_date: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)
    disabled: bool = Field(default=False)

    permissions: Optional[List["Permission"]] = Relationship(back_populates="users", link_model=PermissionUserLink,
                                                             sa_relationship_kwargs={'lazy': 'selectin'})

    def __str__(self):
        return self.email


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    disabled: bool
    permissions: List["PermissionRead"]
    registration_date: datetime.datetime


class UserUpdate(UserBase):
    pass


# -----------------
# ----- Token -----
# -----------------

class Token(SQLModel):
    access_token: str
    token_type: str
