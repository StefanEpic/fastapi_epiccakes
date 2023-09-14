from aiogram import types

from core.keyboards import menu_keyboard


async def start(message: types.Message):
    await message.reply(
        f"Привет, {message.from_user.first_name}!"
        f"\nЭто приватный бот для сотрудников EpicCakes!"
        f"\nЗдесь можно быстро получить данные менеджеров по номеру телефона или почте",
        reply_markup=menu_keyboard()
    )


async def menu(message: types.Message):
    await message.reply(
        'Какую информацию надо найти?',
        reply_markup=menu_keyboard()
    )
