import os

from fastapi import HTTPException, File
from sqlalchemy.exc import IntegrityError

from config import MEDIA_URL, SITE_URL
from models.store import Category, Product, Image, Customer, CustomerManager, Manufacturer, ManufacturerManager, Order, \
    Review, StaffManager, order_product
from schemas.store import ProductCreate, OrderCreate, OrderUpdate, ProductUpdate
from utils.repository import SQLAlchemyRepository, AddressFilterRepository, UserFilterRepository


class CategoryRepository(SQLAlchemyRepository):
    model = Category


class ProductRepository(SQLAlchemyRepository):
    model = Product

    async def add_one_product(self, data: ProductCreate):
        try:
            res = self.model(**data.model_dump())
            res.categories = []

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

    async def edit_one_product(self, self_id: int, data: ProductUpdate):
        try:
            res = await self.session.get(self.model, self_id)
            if not res:
                raise HTTPException(status_code=404, detail="Not found")
            categories = data.categories
            data.categories = []
            res_data = data.model_dump(exclude_unset=True)

            for key, value in res_data.items():
                setattr(res, key, value)

            if categories:
                for cat_id in categories:
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


class CustomerRepository(AddressFilterRepository):
    model = Customer


class CustomerManagerRepository(UserFilterRepository):
    model = CustomerManager


class ManufacturerRepository(AddressFilterRepository):
    model = Manufacturer


class ManufacturerManagerRepository(UserFilterRepository):
    model = ManufacturerManager


class OrderRepository(SQLAlchemyRepository):
    model = Order

    async def add_one_order(self, data: OrderCreate):
        try:
            for product in data.products:
                prod_res = await self.session.get(Product, product)
                if not prod_res:
                    raise HTTPException(status_code=404, detail="Product with this id not found")

            res = self.model(**data.model_dump(exclude={"products"}))
            self.session.add(res)
            await self.session.commit()

            res.sum_price = 0
            for product in data.products:
                prod_res = await self.session.get(Product, product)
                quantity = data.products[product]
                order_res = order_product.insert().values(order_id=res.id, product_id=product, quantity=quantity)
                await self.session.execute(order_res)
                res.sum_price += quantity * prod_res.price

            await self.session.commit()
            await self.session.refresh(res)
            return res
        except ValueError as e:
            raise HTTPException(status_code=200, detail=str(e))
        except IntegrityError as e:
            raise HTTPException(status_code=200, detail=str(e.orig))

    async def edit_one_order(self, self_id: int, data: OrderUpdate):
        try:
            res = await self.session.get(self.model, self_id)
            if not res:
                raise HTTPException(status_code=404, detail="Not found")

            products = data.products
            data.products = []
            res_data = data.model_dump(exclude_unset=True, warnings=False)

            for key, value in res_data.items():
                setattr(res, key, value)

            self.session.add(res)
            await self.session.commit()

            if products:
                res.sum_price = 0
                for product in products:
                    prod_res = await self.session.get(Product, product)
                    if not prod_res:
                        raise HTTPException(status_code=404, detail="Product with this id not found")
                    quantity = products[product]
                    order_res = order_product.insert().values(order_id=res.id, product_id=product, quantity=quantity)
                    await self.session.execute(order_res)
                    res.sum_price += quantity * prod_res.price

            self.session.add(res)
            await self.session.commit()
            await self.session.refresh(res)
            return res
        except ValueError as e:
            raise HTTPException(status_code=200, detail=str(e))
        except IntegrityError as e:
            raise HTTPException(status_code=200, detail=str(e.orig))


class ReviewRepository(SQLAlchemyRepository):
    model = Review


class StaffManagerRepository(UserFilterRepository):
    model = StaffManager


class ImageRepository(SQLAlchemyRepository):
    model = Image

    async def add_one_image(self, product_id: int, image: File):
        try:
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

    async def delete_one_image(self, self_id: int):
        res = await self.session.get(self.model, self_id)
        if not res:
            raise HTTPException(status_code=404, detail="Not found")
        os.remove(res.path)
        await self.session.delete(res)
        await self.session.commit()
        return {"detail": "success"}
