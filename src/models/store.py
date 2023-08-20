import enum
import datetime

from pydantic import condecimal
from typing import Optional, List, Dict

from sqlalchemy.orm import validates
from sqlmodel import SQLModel, Field, Relationship

from utils.validators import name_valid, phone_valid, email_valid, rating_valid


# -------------------------------
# ----- CategoryProductLink -----
# -------------------------------
class CategoryProductLink(SQLModel, table=True):
    category_id: Optional[int] = Field(default=None, foreign_key="category.id", primary_key=True)
    product_id: Optional[int] = Field(default=None, foreign_key="product.id", primary_key=True)


# ----------------------------
# ----- OrderProductLink -----
# ----------------------------
class OrderProductLink(SQLModel, table=True):
    order_id: Optional[int] = Field(default=None, foreign_key="order.id", primary_key=True)
    product_id: Optional[int] = Field(default=None, foreign_key="product.id", primary_key=True)
    quantity: int


# --------------------
# ----- Category -----
# --------------------
class CategoryBase(SQLModel):
    title: str = Field(unique=True)
    description: Optional[str]


class Category(CategoryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    products: List["Product"] = Relationship(back_populates="categories", link_model=CategoryProductLink)

    def __str__(self):
        return self.title


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: int


class CategoryUpdate(SQLModel):
    title: Optional[str] = Field(unique=True)
    description: Optional[str]


# --------------------
# ----- Customer -----
# --------------------
class CustomerStatus(enum.Enum):
    active = "Действующий"
    inactive = "Недействующий"


class CustomerBase(SQLModel):
    title: str = Field(unique=True)
    description: Optional[str]
    city: str
    street: str
    house: str
    office: Optional[str]
    metro_station: Optional[str]
    website: Optional[str]
    status: CustomerStatus


class Customer(CustomerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    registration_date: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)

    managers: List["CustomerManager"] = Relationship(back_populates="customer",
                                                     sa_relationship_kwargs={'lazy': 'selectin'})
    orders: List["Order"] = Relationship(back_populates="customer", sa_relationship_kwargs={'lazy': 'selectin'})
    reviews: List["Review"] = Relationship(back_populates="customer", sa_relationship_kwargs={'lazy': 'selectin'})

    def __str__(self):
        return self.title


class CustomerCreate(CustomerBase):
    pass


class CustomerRead(CustomerBase):
    id: int
    registration_date: datetime.datetime


class CustomerUpdate(SQLModel):
    title: Optional[str] = Field(unique=True)
    description: Optional[str]
    city: Optional[str]
    street: Optional[str]
    house: Optional[str]
    office: Optional[str]
    metro_station: Optional[str]
    website: Optional[str]
    status: Optional[CustomerStatus]


# ---------------------------
# ----- CustomerManager -----
# ---------------------------
class CustomerManagerBase(SQLModel):
    first_name: str
    second_name: str
    last_name: str
    phone: str = Field(unique=True, max_length=12)
    email: str = Field(unique=True)

    customer_id: int = Field(foreign_key="customer.id")

    @validates("first_name", "second_name", "last_name")
    def validate_name(self, key, *names):
        for name in names:
            return name_valid(name)

    @validates("phone")
    def validate_phone(self, key, phone):
        return phone_valid(phone)

    @validates("email")
    def validate_email(self, key, email):
        return email_valid(email)


class CustomerManager(CustomerManagerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    registration_date: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)

    customer: Customer = Relationship(back_populates="managers")

    def __str__(self):
        return f'{self.second_name} {self.first_name[0]}. {self.last_name[0]}.'


class CustomerManagerCreate(CustomerManagerBase):
    pass


class CustomerManagerRead(CustomerManagerBase):
    id: int
    registration_date: datetime.datetime


class CustomerManagerUpdate(SQLModel):
    first_name: Optional[str]
    second_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str] = Field(unique=True, max_length=12)
    email: Optional[str] = Field(unique=True)

    customer_id: Optional[int] = Field(foreign_key="customer.id")


class CustomerReadWithManagers(CustomerRead):
    managers: List[CustomerManagerRead] = []


# ------------------------
# ----- Manufacturer -----
# ------------------------
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

    managers: List["ManufacturerManager"] = Relationship(back_populates="manufacturer",
                                                         sa_relationship_kwargs={'lazy': 'selectin'})
    products: List["Product"] = Relationship(back_populates="manufacturer", sa_relationship_kwargs={'lazy': 'selectin'})

    def __str__(self):
        return self.title


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


# -------------------------------
# ----- ManufacturerManager -----
# -------------------------------
class ManufacturerManagerBase(SQLModel):
    first_name: str
    second_name: str
    last_name: str
    phone: str = Field(unique=True, max_length=12)
    email: str = Field(unique=True)

    manufacturer_id: int = Field(foreign_key="manufacturer.id")

    @validates("first_name", "second_name", "last_name")
    def validate_name(self, key, *names):
        for name in names:
            return name_valid(name)

    @validates("phone")
    def validate_phone(self, key, phone):
        return phone_valid(phone)

    @validates("email")
    def validate_email(self, key, email):
        return email_valid(email)


class ManufacturerManager(ManufacturerManagerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    registration_date: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)

    manufacturer: Manufacturer = Relationship(back_populates="managers")

    def __str__(self):
        return f'{self.second_name} {self.first_name[0]}. {self.last_name[0]}.'


class ManufacturerManagerCreate(ManufacturerManagerBase):
    pass


class ManufacturerManagerRead(ManufacturerManagerBase):
    id: int
    registration_date: datetime.datetime


class ManufacturerManagerUpdate(SQLModel):
    first_name: Optional[str]
    second_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str] = Field(unique=True, max_length=12)
    email: Optional[str] = Field(unique=True)

    manufacturer_id: Optional[int] = Field(foreign_key="manufacturer.id")


class ManufacturerReadWithManagers(ManufacturerRead):
    managers: List[ManufacturerManagerRead] = []


# ------------------------
# ----- StaffManager -----
# ------------------------
class JobTitle(enum.Enum):
    intern = "Стажер"
    junior = "Младший специалист"
    middle = "Специалист"
    senior = "Ведущий специалист"


class StaffManagerBase(SQLModel):
    first_name: str
    second_name: str
    last_name: str
    phone: str = Field(unique=True, max_length=12)
    email: str = Field(unique=True)
    job_title: JobTitle

    @validates("first_name", "second_name", "last_name")
    def validate_name(self, key, *names):
        for name in names:
            return name_valid(name)

    @validates("phone")
    def validate_phone(self, key, phone):
        return phone_valid(phone)

    @validates("email")
    def validate_email(self, key, email):
        return email_valid(email)


class StaffManager(StaffManagerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    registration_date: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)

    orders: List["Order"] = Relationship(back_populates="staffmanagers", sa_relationship_kwargs={'lazy': 'selectin'})

    def __str__(self):
        return f'{self.second_name} {self.first_name[0]}. {self.last_name[0]}.'


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


# -------------------
# ----- Product -----
# -------------------
class ProductType(enum.Enum):
    biscuit = "Бисквитные"
    sandy = "Песочные"
    puff = "Слоеные"
    waffle = "Вафельные"
    air = "Воздушные"
    tiny = "Крошковые"
    custards = "Заварные"


class ProductBase(SQLModel):
    title: str = Field(unique=True)
    type: ProductType
    weight: Optional[int]
    best_before_date: Optional[int]
    storage_temperature: Optional[int]
    proteins: Optional[int]
    fats: Optional[int]
    carbohydrates: Optional[int]
    energy_value: Optional[int]
    description: Optional[str]
    # price: condecimal(max_digits=8, decimal_places=2) = Field(default=0)
    price: float

    manufacturer_id: int = Field(foreign_key="manufacturer.id")


class Product(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    images: List["Image"] = Relationship(back_populates="product", sa_relationship_kwargs={'lazy': 'selectin'})
    manufacturer: Manufacturer = Relationship(back_populates="products")
    categories: List["Category"] = Relationship(back_populates="products", link_model=CategoryProductLink,
                                                sa_relationship_kwargs={'lazy': 'selectin'})
    orders: List["Order"] = Relationship(back_populates="products", link_model=OrderProductLink)

    def __str__(self):
        return self.title


class ProductCreate(ProductBase):
    categories: List[int]


class ProductRead(ProductBase):
    id: int


class ProductUpdate(SQLModel):
    title: Optional[str] = Field(unique=True)
    type: Optional[ProductType]
    weight: Optional[int]
    best_before_date: Optional[int]
    storage_temperature: Optional[int]
    proteins: Optional[int]
    fats: Optional[int]
    carbohydrates: Optional[int]
    energy_value: Optional[int]
    description: Optional[str]
    # price: Optional[condecimal]
    price: Optional[float]

    manufacturer_id: Optional[int] = Field(foreign_key="manufacturer.id")
    categories: Optional[List[int]]


# -----------------
# ----- Image -----
# -----------------
class ImageBase(SQLModel):
    title: str = Field(unique=True)
    url: str

    product_id: int = Field(foreign_key="product.id")


class Image(ImageBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    path: str
    product: Product = Relationship(back_populates="images")

    def __str__(self):
        return self.title


class ImageRead(ImageBase):
    id: int


class ProductReadWithCategoriesAndImages(ProductRead):
    categories: List[CategoryRead] = []
    images: List[ImageRead] = []


# -----------------
# ----- Order -----
# -----------------
class OrderDelivery(enum.Enum):
    delivery = "Доставка"
    pickup = "Самовывоз"


class OrderPay(enum.Enum):
    cash = "Наличными"
    card = "Банковской картой"


class OrderStatus(enum.Enum):
    processing = "В работе"
    done = "Выполнено"


class OrderBase(SQLModel):
    delivery_method: OrderDelivery
    payment_method: OrderPay
    status: OrderStatus

    staffmanager_id: int = Field(foreign_key="staffmanager.id")
    customer_id: int = Field(foreign_key="customer.id")


class Order(OrderBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)
    sum_price: float = Field(default=0)

    staffmanagers: StaffManager = Relationship(back_populates="orders")
    reviews: List["Review"] = Relationship(back_populates="order", sa_relationship_kwargs={'lazy': 'selectin'})
    customer: Customer = Relationship(back_populates="orders")
    products: List["Product"] = Relationship(back_populates="orders", link_model=OrderProductLink,
                                             sa_relationship_kwargs={'lazy': 'selectin'})

    def __str__(self):
        return f'{self.customer_id} / {self.status}'


class OrderCreate(OrderBase):
    products: Dict[int, int]


class OrderRead(OrderBase):
    id: int
    date: datetime.datetime
    sum_price: float


class OrderUpdate(SQLModel):
    delivery_method: Optional[OrderDelivery]
    payment_method: Optional[OrderPay]
    status: Optional[OrderStatus]

    staffmanager_id: Optional[int] = Field(foreign_key="staffmanager.id")
    customer_id: Optional[int] = Field(foreign_key="customer.id")
    products: Optional[Dict[int, int]]


class OrderReadWithProducts(OrderRead):
    products: List[ProductRead] = []


class StaffManagerReadWithOrders(StaffManagerRead):
    orders: List[OrderRead] = []


# ------------------
# ----- Review -----
# ------------------
class ReviewBase(SQLModel):
    rating: int = Field(default=0)
    text: str

    order_id: int = Field(foreign_key="order.id")
    customer_id: int = Field(foreign_key="customer.id")

    @validates("rating")
    def validate_rating(self, key, rating):
        return rating_valid(rating)


class Review(ReviewBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date_in: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)

    order: Order = Relationship(back_populates="reviews")
    customer: Customer = Relationship(back_populates="reviews")

    def __str__(self):
        return f'{self.rating} / {self.text[:20]}...'


class ReviewCreate(ReviewBase):
    pass


class ReviewRead(ReviewBase):
    id: int
    date_in: datetime.datetime


class ReviewUpdate(SQLModel):
    rating: Optional[int] = Field(default=0)
    text: Optional[str]
