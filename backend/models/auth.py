from typing import List

from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base, AbstractUser

permission_user = Table(
    "permission_user",
    Base.metadata,
    Column("permission_id", ForeignKey("permission.id")),
    Column("user_id", ForeignKey("user.id")),
)


class Permission(Base):
    __tablename__ = "permission"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)

    users: Mapped[List["User"]] = relationship(secondary=permission_user,
                                               back_populates="permissions",
                                               lazy="selectin")

    def __str__(self):
        return self.title


class User(AbstractUser):
    __tablename__ = "user"

    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    permissions: Mapped[List["Permission"]] = relationship(secondary=permission_user,
                                                           back_populates="users",
                                                           lazy="selectin")
