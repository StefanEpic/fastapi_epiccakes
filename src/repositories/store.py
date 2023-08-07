from models.store import Manufacturer
from utils.repository import SQLAlchemyRepository


class ManufacturerRepository(SQLAlchemyRepository):
    model = Manufacturer
