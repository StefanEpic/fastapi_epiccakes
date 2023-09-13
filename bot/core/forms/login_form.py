import requests
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from config import SITE_URL
from core.db import users_tokens


class LoginForm(StatesGroup):
    GET_USERNAME = State()
    GET_PASSWORD = State()


async def get_username(message: Message, state: FSMContext):
    await message.reply("Введите Ваш логин:")
    await state.set_state(LoginForm.GET_USERNAME)


async def get_password(message: Message, state: FSMContext):
    await message.reply("Введите Ваш пароль:")
    await state.update_data(username=message.text)
    await state.set_state(LoginForm.GET_PASSWORD)


async def login(message: Message, state: FSMContext):
    data = await state.get_data()
    username = data.get("username")
    password = message.text
    response = requests.post(f"{SITE_URL}/token",
                             data={
                                 "username": username,
                                 "password": password
                             },
                             headers={"content-type": "application/x-www-form-urlencoded"})
    if response.status_code == 200:
        token = response.json()['access_token']
        users_tokens[message.from_user.id] = token
        await message.reply("Авторизация успешна!")
    else:
        await message.reply("Ошибка авторизации!")

    await state.clear()
