from abc import ABC, abstractmethod

from sqlmodel import select, insert


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
        res = await self.session.execute(stmt).all()
        return res

    async def select_one(self, self_id: int):
        res = await self.session.get(self.model, self_id)
        if not res:
            raise HTTPException(status_code=404, detail="Not found")
        return res
    
    async def add_one(self, data):
        res = self.model.from_orm(data)
        self.session.add(res)
        await self.session.commit()
        await self.session.refresh(res)
        return res
    
    async def edit_one(self, self_id: int, data):
        res = await self.session.get(self_id, data)
        if not res:
            raise HTTPException(status_code=404, detail="Not found")
        res_data = self.model.dict(exclude_unset=True)
        for key, value in res_data.items():
            setattr(res, key, value)
        self.session.add(res)
        await self.session.commit()
        await self.session.refresh(res)
        return res
    
    async def delete_one(self, self_id: int):
        res = await self.session.get(self.model, self_id)
        if not res:
            raise HTTPException(status_code=404, detail="Not found")
        self.session.delete(res)
        await self.session.commit()
        return {"ok": True}
        
