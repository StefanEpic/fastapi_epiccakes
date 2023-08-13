import os

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from db.db import MEDIA_URL, SITE_URL
from models.store import Category, Product, Image, Client, ClientManager, Manufacturer, ManufacturerManager, Order, \
    Review, StaffManager, CategoryProductLink
from utils.repository import SQLAlchemyRepository


class CategoryRepository(SQLAlchemyRepository):
    model = Category


class ProductRepository(SQLAlchemyRepository):
    model = Product

    async def add_one(self, data):
        try:
            res = self.model.from_orm(data)

            for cat_id in data.categories:
                cat_res = await self.session.get(Category, cat_id)
                if not cat_res:
                    raise HTTPException(status_code=404, detail="Category with this id not found")
                res.categories.append(cat_res)

            self.session.add(res)
            await self.session.commit()
            await self.session.refresh(res)
            return res
        except ValueError as e:
            raise HTTPException(status_code=200, detail=str(e))
        except IntegrityError as e:
            raise HTTPException(status_code=200, detail=str(e.orig))


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


class ImageRepository(SQLAlchemyRepository):
    model = Image

    async def add_one(self, product_id, image):
        try:
            p_id = await self.session.get(Product, product_id)
            if not p_id:
                raise HTTPException(status_code=404, detail="Product with this id not found")

            contents = await image.read()
            filepath = f'{MEDIA_URL}/{image.filename}'
            url = SITE_URL + '/media/' + image.filename
            res = Image(title=image.filename, path=filepath, product_id=product_id, url=url)
            self.session.add(res)
            await self.session.commit()
            await self.session.refresh(res)

            with open(filepath, "wb") as f:
                f.write(contents)
            return res
        except ValueError as e:
            raise HTTPException(status_code=200, detail=str(e))
        except IntegrityError as e:
            raise HTTPException(status_code=200, detail=str(e.orig))

    async def delete_one(self, self_id: int):
        res = await self.session.get(self.model, self_id)
        if not res:
            raise HTTPException(status_code=404, detail="Not found")
        os.remove(res.path)
        await self.session.delete(res)
        await self.session.commit()
        return {"result": "success"}
