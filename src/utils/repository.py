from abc import ABC, abstractmethod

from fastapi import HTTPException
from sqlmodel import select


class AbstractRepository(ABC):
    @abstractmethod
    async def get_list(self):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session):
        self.session = session

    async def get_list(self):
        stmt = select(self.model)
        res = await self.session.execute(stmt)
        res = [row[0] for row in res.all()]
        return res

    async def get_one(self, self_id: int):
        res = await self.session.get(self.model, self_id)
        if not res:
            raise HTTPException(status_code=404, detail="Not found")
        return res

    async def add_one(self, data):
        try:
            res = self.model.from_orm(data)
            self.session.add(res)
            await self.session.commit()
            await self.session.refresh(res)
            return res.id
        except ValueError as error:
            raise HTTPException(status_code=200, detail=str(error))

    async def edit_one(self, self_id: int, data):
        try:
            res = await self.session.get(self.model, self_id)
            if not res:
                raise HTTPException(status_code=404, detail="Not found")
            res_data = data.dict(exclude_unset=True)
            for key, value in res_data.items():
                setattr(res, key, value)
            self.session.add(res)
            await self.session.commit()
            await self.session.refresh(res)
            return res
        except ValueError as error:
            raise HTTPException(status_code=200, detail=str(error))

    async def delete_one(self, self_id: int):
        res = await self.session.get(self.model, self_id)
        if not res:
            raise HTTPException(status_code=404, detail="Not found")
        await self.session.delete(res)
        await self.session.commit()
        return {"ok": True}
