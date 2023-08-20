from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from sqlmodel.ext.asyncio.session import AsyncSession

from db.db import get_session
from models.auth import Token
from utils.auth import login_for_access_token, get_current_user

router = APIRouter(
    prefix="",
    tags=["Auth"],
)


@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                session: AsyncSession = Depends(get_session)):
    return await login_for_access_token(form_data, session)


@router.get("/logout")
async def logout(current_user: Token = Depends(get_current_user)):
    return {"detail": "success"}
