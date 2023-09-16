import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from core.commands.base import start_bot
from core.commands.callback import manufacturer, customer
from core.commands.commands import start, menu
from core.forms.find_form import get_manufacturer_email, get_manufacturer_phone, manufacturer_email_find, \
    manufacturer_phone_find, ManufacturerEmailFindForm, ManufacturerPhoneFindForm, get_customer_email, \
    get_customer_phone, customer_email_find, customer_phone_find, CustomerEmailFindForm, CustomerPhoneFindForm
from core.forms.login_form import get_username, get_password, LoginForm, login


async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.startup.register(start_bot)
    dp.message.register(start, Command(commands='start'))
    dp.message.register(menu, Command(commands='menu'))

    dp.callback_query.register(get_username, F.data.startswith('login'))
    dp.message.register(get_password, LoginForm.GET_USERNAME)
    dp.message.register(login, LoginForm.GET_PASSWORD)

    dp.callback_query.register(manufacturer, F.data.startswith('manufacturer'))
    dp.callback_query.register(get_manufacturer_email, F.data.startswith('m_email'))
    dp.callback_query.register(get_manufacturer_phone, F.data.startswith('m_phone'))
    dp.message.register(manufacturer_email_find, ManufacturerEmailFindForm.GET_FIND)
    dp.message.register(manufacturer_phone_find, ManufacturerPhoneFindForm.GET_FIND)

    dp.callback_query.register(customer, F.data.startswith('customer'))
    dp.callback_query.register(get_customer_email, F.data.startswith('c_email'))
    dp.callback_query.register(get_customer_phone, F.data.startswith('c_phone'))
    dp.message.register(customer_email_find, CustomerEmailFindForm.GET_FIND)
    dp.message.register(customer_phone_find, CustomerPhoneFindForm.GET_FIND)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
