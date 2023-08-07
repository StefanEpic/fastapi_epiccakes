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
        res = await self.session.execute(stmt)
        res = [row[0] for row in res.all()]
        return res


    # async def select_one(self, **filter_by):
    #     async with async_session_maker() as session:
    #         stmt = select(self.model).filter_by(**filter_by)
    #         res = await session.execute(stmt)
    #         res = res.one_or_none()
    #         if res:
    #             res = res[0].to_read_model()
    #         return {"status": 200, "detail": res}
    #
    # async def add_one(self, data) -> int:
    #     async with async_session_maker() as session:
    #         session.add(data)
    #         await session.commit()
    #         await session.refresh(data)
    #         return {"status": 200, "detail": data.id}
    #
    # async def edit_one(self, data: dict, **filter_by):
    #     async with async_session_maker() as session:
    #         stmt = update(self.model).filter_by(**filter_by).values(**data).returning(self.model.id)
    #         res = await session.execute(stmt)
    #         await session.commit()
    #         res = res.scalar_one()
    #         return {"status": 200, "detail": res}
    #
    # async def delete_oneself, **filter_by) -> int:
    #     async with async_session_maker() as session:
    #         stmt = delete(self.model).filter_by(**filter_by).returning(self.model.id)
    #         res = await session.execute(stmt)
    #         await session.delete()
    #         await session.commit()
    #         return {"status": 200, "detail": res.scalar_one()}
