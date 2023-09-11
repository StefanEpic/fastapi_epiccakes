import asyncio
import json
import logging

import requests
from aiogram import Bot, Dispatcher, types, Router
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage

TOKEN = ''

router = Router()

SITE_URL = 'http://31.129.98.245'
user_tokens = {}


@router.message(Command("start"))
async def start(message: types.Message):
    await message.reply(
        f"Привет, {message.from_user.first_name}! Для авторизации отправьте свой username и password в формате: /login username password")


@router.message(Command("login"))
async def login(message: types.Message):
    try:
        _, username, password = message.text.split()
        response = requests.post(f"{SITE_URL}/token",
                                 data={
                                     "username": username,
                                     "password": password
                                 },
                                 headers={"content-type": "application/x-www-form-urlencoded"})
        if response.status_code == 200:
            token = response.json()['access_token']
            user_tokens[message.from_user.id] = token
            await message.reply("Авторизация успешна!")
        else:
            await message.reply("Ошибка авторизации")
    except ValueError:
        await message.reply("Неверный формат команды. Используйте: /auth username password")


@router.message(Command("users"))
async def users(message: types.Message):
    response = requests.get(f"{SITE_URL}/users",
                            headers={"Authorization": f"Bearer {user_tokens[message.from_user.id]}"})
    if response.status_code == 200:
        await message.reply(json.dumps(response.json()))
    else:
        await message.reply("Ошибка авторизации")


async def main():
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
