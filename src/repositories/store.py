from models.store import Category, Product, Image, Client, ClientManager, Manufacturer, ManufacturerManager, Order, Review
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
