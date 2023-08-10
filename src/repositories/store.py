from models.store import Category, Product, Image, Client, ClientManager, Manufacturer, ManufacturerManager, Order, Review, StaffManager
from utils.repository import SQLAlchemyRepository


class CategoryRepository(SQLAlchemyRepository):
    model = Category


class ProductRepository(SQLAlchemyRepository):
    model = Product


class ImageRepository(SQLAlchemyRepository):
    model = Image


class ClientRepository(SQLAlchemyRepository):
    model = Client


class ClientManagerRepository(SQLAlchemyRepository):
    model = ClientManager


class ManufacturerRepository(SQLAlchemyRepository):
    model = Manufacturer


class ManufacturerManagerRepository(SQLAlchemyRepository):
    model = ManufacturerManager


class OrderRepository(SQLAlchemyRepository):
    model = Order


class ReviewRepository(SQLAlchemyRepository):
    model = Review


class StaffManagerRepository(SQLAlchemyRepository):
    model = StaffManager

