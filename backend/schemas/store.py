import datetime
from typing import List, Dict, Optional

from pydantic import BaseModel

from models.enums import JobTitle, ProductType, OrderDelivery, OrderPay, OrderStatus
from schemas.base import AbstractCompanyCreate, AbstractCompanyRead, AbstractCompanyUpdate, AbstractUserCreate, \
    AbstractUserRead, AbstractUserUpdate


class CustomerCreate(AbstractCompanyCreate):
    pass


class CustomerRead(AbstractCompanyRead):
    pass


class CustomerUpdate(AbstractCompanyUpdate):
    pass


class ManufacturerCreate(AbstractCompanyCreate):
    pass


class ManufacturerRead(AbstractCompanyRead):
    pass


class ManufacturerUpdate(AbstractCompanyUpdate):
    pass


class CustomerManagerCreate(AbstractUserCreate):
    customer_id: int
    phone: str


class CustomerManagerRead(AbstractUserRead):
    customer_id: int
    phone: str


class CustomerManagerUpdate(AbstractUserUpdate):
    customer_id: Optional[int] = None
    phone: Optional[str] = None


class CustomerReadWithManagers(CustomerRead):
    managers: Optional[List[CustomerManagerRead]] = None


class ManufacturerManagerCreate(AbstractUserCreate):
    manufacturer_id: int
    phone: str


class ManufacturerManagerRead(AbstractUserRead):
    manufacturer_id: int
    phone: str


class ManufacturerManagerUpdate(AbstractUserUpdate):
    manufacturer_id: Optional[int] = None
    phone: Optional[str] = None


class ManufacturerReadWithManagers(ManufacturerRead):
    managers: Optional[List[ManufacturerManagerRead]] = None


class StaffManagerCreate(AbstractUserCreate):
    job_title: JobTitle
    phone: str


class StaffManagerRead(AbstractUserRead):
    job_title: JobTitle
    phone: str


class StaffManagerUpdate(AbstractUserUpdate):
    job_title: Optional[JobTitle] = None
    phone: Optional[str] = None


class CategoryCreate(BaseModel):
    title: str
    description: Optional[str] = None


class CategoryRead(BaseModel):
    id: int
    title: str
    description: Optional[str] = None


class CategoryUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class ProductCreate(BaseModel):
    title: str
    type: ProductType
    weight: Optional[int] = None
    best_before_date: Optional[int] = None
    storage_temperature: Optional[int] = None
    proteins: Optional[int] = None
    fats: Optional[int] = None
    carbohydrates: Optional[int] = None
    energy_value: Optional[int] = None
    description: Optional[str] = None
    price: float
    categories: List[int]
    manufacturer_id: int


class ProductRead(BaseModel):
    id: int
    title: str
    type: ProductType
    weight: Optional[int] = None
    best_before_date: Optional[int] = None
    storage_temperature: Optional[int] = None
    proteins: Optional[int] = None
    fats: Optional[int] = None
    carbohydrates: Optional[int] = None
    energy_value: Optional[int] = None
    description: Optional[str] = None
    price: float
    categories: List["CategoryRead"]
    manufacturer_id: int


class ProductUpdate(BaseModel):
    title: Optional[str] = None
    type: Optional[ProductType] = None
    weight: Optional[int] = None
    best_before_date: Optional[int] = None
    storage_temperature: Optional[int] = None
    proteins: Optional[int] = None
    fats: Optional[int] = None
    carbohydrates: Optional[int] = None
    energy_value: Optional[int] = None
    description: Optional[str] = None
    price: Optional[float] = None
    categories: List[int] = None
    manufacturer_id: Optional[int] = None


class ImageCreate(BaseModel):
    title: str
    url: str
    product_id: int


class ImageRead(BaseModel):
    id: int
    title: str
    url: str
    product_id: int


class ImageUpdate(BaseModel):
    title: Optional[str] = None
    url: Optional[str] = None
    product_id: Optional[int] = None


class ProductReadWithCategoriesAndImages(ProductRead):
    categories: Optional[List[CategoryRead]] = None
    images: Optional[List[ImageRead]] = None


class OrderCreate(BaseModel):
    delivery_method: OrderDelivery
    payment_method: OrderPay
    products: Dict[int, int]
    staff_manager_id: int
    customer_id: int


class OrderRead(BaseModel):
    id: int
    delivery_method: OrderDelivery
    payment_method: OrderPay
    status: OrderStatus
    date: datetime.datetime
    sum_price: float
    products: List["ProductRead"]
    staff_manager_id: int
    customer_id: int


class OrderUpdate(BaseModel):
    delivery_method: Optional[OrderDelivery] = None
    payment_method: Optional[OrderPay] = None
    status: Optional[OrderStatus] = None
    products: Optional[Dict[int, int]] = None
    staff_manager_id: Optional[int] = None
    customer_id: Optional[int] = None


class OrderReadWithProducts(OrderRead):
    products: Optional[List[ProductRead]] = None


class StaffManagerReadWithOrders(StaffManagerRead):
    orders: Optional[List[OrderRead]] = None


class ReviewCreate(BaseModel):
    rating: int
    text: str
    order_id: int
    customer_id: int


class ReviewRead(BaseModel):
    id: int
    rating: int
    text: str
    date_in: datetime.datetime
    order_id: int
    customer_id: int


class ReviewUpdate(BaseModel):
    rating: Optional[int] = None
    text: Optional[str] = None
