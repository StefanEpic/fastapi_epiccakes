from abc import ABC, abstractmethod
from typing import List, Dict

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    @abstractmethod
    async def get_list(self):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_list(self, offset: int, limit: int) -> List[BaseModel]:
        stmt = select(self.model).offset(offset).limit(limit)
        res = await self.session.execute(stmt)
        res = [row[0] for row in res.all()]
        return res

    async def get_one(self, self_id: int) -> BaseModel:
        res = await self.session.get(self.model, self_id)
        if not res:
            raise HTTPException(status_code=404, detail="Not found")
        return res

    async def add_one(self, data: BaseModel) -> BaseModel:
        try:
            res = self.model(**data.model_dump())
            self.session.add(res)
            await self.session.commit()
            await self.session.refresh(res)
            return res
        except ValueError as e:
            raise HTTPException(status_code=200, detail=str(e))
        except IntegrityError as e:
            raise HTTPException(status_code=200, detail=str(e.orig))

    async def edit_one(self, self_id: int, data: BaseModel) -> BaseModel:
        try:
            res = await self.session.get(self.model, self_id)
            if not res:
                raise HTTPException(status_code=404, detail="Not found")
            res_data = data.model_dump(exclude_unset=True)
            for key, value in res_data.items():
                setattr(res, key, value)
            self.session.add(res)
            await self.session.commit()
            await self.session.refresh(res)
            return res
        except ValueError as e:
            raise HTTPException(status_code=200, detail=str(e))

    async def delete_one(self, self_id: int) -> Dict:
        res = await self.session.get(self.model, self_id)
        if not res:
            raise HTTPException(status_code=404, detail="Not found")
        await self.session.delete(res)
        await self.session.commit()
        return {"detail": "success"}


class AddressFilterRepository(SQLAlchemyRepository):
    async def get_address_filter_list(self, offset: int, limit: int, city: str, street: str, metro_station: str) -> \
            List[BaseModel]:
        stmt = select(self.model).offset(offset).limit(limit)
        res = await self.session.execute(stmt)
        res = [row[0] for row in res.all()]
        if city:
            res = list(filter(lambda x: x.city == city, res))
        if street:
            res = list(filter(lambda x: x.street == street, res))
        if metro_station:
            res = list(filter(lambda x: x.metro_station == metro_station, res))
        return res


class UserFilterRepository(SQLAlchemyRepository):
    async def get_user_filter_list(self, offset: int, limit: int, phone: str, email: str) -> List[BaseModel]:
        stmt = select(self.model).offset(offset).limit(limit)
        res = await self.session.execute(stmt)
        res = [row[0] for row in res.all()]
        if phone:
            res = list(filter(lambda x: x.phone == phone, res))
        if email:
            res = list(filter(lambda x: x.email == email, res))
        return res
