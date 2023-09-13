import json

import requests
from aiogram import types

from config import SITE_URL
from core.db import users_tokens


async def start(message: types.Message):
    await message.reply(
        f"Привет, {message.from_user.first_name}!"
        f"\nЭто приватный бот для сотрудников EpicCakes!"
        f"\nЗдесь можно быстро получить данные менеджеров по номеру телефона или почте"
    )


async def users(message: types.Message):
    response = requests.get(f"{SITE_URL}/users",
                            headers={"Authorization": f"Bearer {users_tokens[message.from_user.id]}"})
    if response.status_code == 200:
        await message.reply(json.dumps(response.json()))
    else:
        await message.reply("Ошибка авторизации")
