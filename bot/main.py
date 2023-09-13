import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from core.commands import start, users
from core.forms.login_form import get_username, get_password, LoginForm, login


async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.message.register(start, Command(commands='start'))

    dp.message.register(get_username, Command(commands='login'))
    dp.message.register(get_password, LoginForm.GET_USERNAME)
    dp.message.register(login, LoginForm.GET_PASSWORD)

    dp.message.register(users, Command(commands='users'))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
