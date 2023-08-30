from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from models.auth import User, UserCreate
from utils.auth import Hasher
from utils.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = User

    async def add_one_user(self, user: UserCreate):
        try:
            hashed_password = Hasher.get_password_hash(user.password)
            new_user = User(first_name=user.first_name,
                            second_name=user.second_name,
                            last_name=user.last_name,
                            phone=user.phone,
                            email=user.email,
                            hashed_password=hashed_password)
            self.session.add(new_user)
            await self.session.commit()
            await self.session.refresh(new_user)
            return new_user
        except ValueError as e:
            raise HTTPException(status_code=200, detail=str(e))
        except IntegrityError as e:
            raise HTTPException(status_code=200, detail=str(e.orig))

    async def edit_one_user(self, user_id: int, user: UserCreate):
        try:
            res = await self.session.get(User, user_id)
            if not res:
                raise HTTPException(status_code=404, detail="Not found")
            res_data = user.dict(exclude_unset=True)
            hashed_password = Hasher.get_password_hash(res_data.pop("password"))
            res_data.update({'hashed_password': hashed_password})

            for key, value in res_data.items():
                setattr(res, key, value)

            self.session.add(res)
            await self.session.commit()
            await self.session.refresh(res)
            return res
        except ValueError as e:
            raise HTTPException(status_code=200, detail=str(e))
