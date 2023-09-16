from urllib.parse import quote

import requests
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import SITE_URL
from core.db import db


async def get_find(message: Message, state: FSMContext, title: str, param: str, answer: str):
    try:
        text = quote(message.text)
        token = db.get(message.from_user.id).decode('utf-8')
        response = requests.get(f"{SITE_URL}/{title}_managers?{param}={text}",
                                headers={"Authorization": f"Bearer {token}"})
        user = response.json()
        if user:
            user = user[0]
            response = requests.get(f"{SITE_URL}/{title}s/{user['id']}",
                                    headers={"Authorization": f"Bearer {token}"})
            company = response.json()

            await message.reply(
                f"Фамилия: {user['second_name']}"
                f"\nИмя: {user['first_name']}"
                f"\nОтчество: {user['last_name']}"
                f"\nТелефон: {user['phone']}"
                f"\nПочта: {user['email']}"
                f"\nКомпания: {company['title']}"
            )
        else:
            await message.reply(answer)
    except KeyError:
        await message.reply("Вы не авторизованы!")

    await state.clear()
