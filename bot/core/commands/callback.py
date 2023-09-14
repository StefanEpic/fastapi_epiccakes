from aiogram.types import CallbackQuery

from core.keyboards import manufacturer_keyboard, customer_keyboard


async def manufacturer(call: CallbackQuery):
    await call.message.answer(
        'Найти поставщика по почте или телефону?',
        reply_markup=manufacturer_keyboard()
    )


async def customer(call: CallbackQuery):
    await call.message.answer(
        'Найти покупателя по почте или телефону?',
        reply_markup=customer_keyboard()
    )
