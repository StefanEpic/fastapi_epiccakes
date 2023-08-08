from models.store.category import Category
from models.store.client import Client
from models.store.client_manager import ClientManager
from models.store.image import Image
from models.store.manufacturer import Manufacturer
from models.store.manufacturer_manager import ManufacturerManager
from models.store.order import Order
from models.store.product import Product
from models.store.review import Review

from utils.repository import SQLAlchemyRepository


class CategoryRepository(SQLAlchemyRepository):
    model = Category


class ClientRepository(SQLAlchemyRepository):
    model = Client


class ClientManagerRepository(SQLAlchemyRepository):
    model = ClientManager


class ImageRepository(SQLAlchemyRepository):
    model = Image


class ManufacturerRepository(SQLAlchemyRepository):
    model = Manufacturer


class ManufacturerManagerRepository(SQLAlchemyRepository):
    model = ManufacturerManager


class OrderRepository(SQLAlchemyRepository):
    model = Order


class ProductRepository(SQLAlchemyRepository):
    model = Product


class ReviewRepository(SQLAlchemyRepository):
    model = Review
