import datetime

# from pydantic import condecimal
from typing import Optional, List

from sqlalchemy import Column, ForeignKey, Table, Integer
from sqlalchemy.orm import Mapped, mapped_column, validates, relationship

from models.base import Base, AbstractUser, AbstractCompany
from models.enums import JobTitle, ProductType, OrderDelivery, OrderPay, OrderStatus
from utils.validators import rating_valid

category_product = Table(
    "category_product",
    Base.metadata,
    Column("category_id", ForeignKey("category.id")),
    Column("product_id", ForeignKey("product.id")),
)

order_product = Table(
    "order_product",
    Base.metadata,
    Column("order_id", ForeignKey("order.id")),
    Column("product_id", ForeignKey("product.id")),
    Column("quantity", Integer),
)


class Customer(AbstractCompany):
    __tablename__ = "customer"

    managers: Mapped["CustomerManager"] = relationship(back_populates="customer", lazy="noload")
    orders: Mapped["Order"] = relationship(back_populates="customer")
    reviews: Mapped["Review"] = relationship(back_populates="customer")


class Manufacturer(AbstractCompany):
    __tablename__ = "manufacturer"

    managers: Mapped["ManufacturerManager"] = relationship(back_populates="manufacturer", lazy="noload")
    products: Mapped["Product"] = relationship(back_populates="manufacturer")


class CustomerManager(AbstractUser):
    __tablename__ = "customer_manager"

    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))
    customer: Mapped["Customer"] = relationship(back_populates="managers")


class ManufacturerManager(AbstractUser):
    __tablename__ = "manufacturer_manager"

    manufacturer_id: Mapped[int] = mapped_column(ForeignKey("manufacturer.id"))
    manufacturer: Mapped["Manufacturer"] = relationship(back_populates="managers")


class StaffManager(AbstractUser):
    __tablename__ = "staff_manager"

    job_title: Mapped[JobTitle]

    orders: Mapped["Order"] = relationship(back_populates="staff_manager", lazy='noload')


class Category(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    description: Mapped[Optional[str]]
    products: Mapped[List["Product"]] = relationship(secondary=category_product,
                                                     back_populates="categories",
                                                     lazy="selectin")

    def __str__(self):
        return self.title


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True, index=True)
    type: Mapped[ProductType]
    weight: Mapped[Optional[int]]
    best_before_date: Mapped[Optional[int]]
    storage_temperature: Mapped[Optional[int]]
    proteins: Mapped[Optional[int]]
    fats: Mapped[Optional[int]]
    carbohydrates: Mapped[Optional[int]]
    energy_value: Mapped[Optional[int]]
    description: Mapped[Optional[str]]
    # price: Optional[condecimal]
    price: Mapped[float]

    categories: Mapped[List["Category"]] = relationship(secondary=category_product, lazy="selectin")
    manufacturer_id: Mapped[int] = mapped_column(ForeignKey("manufacturer.id"))
    manufacturer: Mapped["Manufacturer"] = relationship(back_populates="products")
    orders: Mapped[List["Order"]] = relationship(secondary=order_product, back_populates="products", lazy="selectin")
    images: Mapped[List["Image"]] = relationship(back_populates="product", lazy="selectin")

    def __str__(self):
        return self.title


class Image(Base):
    __tablename__ = "image"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    url: Mapped[str]
    path: Mapped[str]

    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    product: Mapped["Product"] = relationship(back_populates="images", lazy="selectin")

    def __str__(self):
        return self.title


class Order(Base):
    __tablename__ = "order"

    id: Mapped[int] = mapped_column(primary_key=True)
    delivery_method: Mapped[OrderDelivery] = mapped_column(index=True)
    payment_method: Mapped[OrderPay] = mapped_column(index=True)
    status: Mapped[OrderStatus] = mapped_column(default=OrderStatus.processing, index=True)
    date: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow)
    sum_price: Mapped[float] = mapped_column(default=0)

    products: Mapped[List["Product"]] = relationship(secondary=order_product, back_populates="orders", lazy="selectin")
    staff_manager_id: Mapped[int] = mapped_column(ForeignKey("staff_manager.id"))
    staff_manager: Mapped["StaffManager"] = relationship(back_populates="orders")
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))
    customer: Mapped["Customer"] = relationship(back_populates="orders")
    reviews: Mapped["Review"] = relationship(back_populates="order")

    def __str__(self):
        return f'{self.customer_id} / {self.status}'


class Review(Base):
    __tablename__ = "review"

    id: Mapped[int] = mapped_column(primary_key=True)
    rating: Mapped[int] = mapped_column(default=0, index=True)
    text: Mapped[str]
    date_in: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow)

    order_id: Mapped[int] = mapped_column(ForeignKey("order.id"))
    order: Mapped["Order"] = relationship(back_populates="reviews")
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))
    customer: Mapped["Customer"] = relationship(back_populates="reviews")

    def __str__(self):
        return f'{self.rating} / {self.text[:20]}...'

    @validates("rating")
    def validate_rating(self, key, rating):
        return rating_valid(rating)
