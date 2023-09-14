from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from core.forms.base import get_find


class ManufacturerEmailFindForm(StatesGroup):
    GET_FIND = State()


class ManufacturerPhoneFindForm(StatesGroup):
    GET_FIND = State()


class CustomerEmailFindForm(StatesGroup):
    GET_FIND = State()


class CustomerPhoneFindForm(StatesGroup):
    GET_FIND = State()


async def get_manufacturer_email(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Введите почту поставщика:")
    await state.set_state(ManufacturerEmailFindForm.GET_FIND)


async def get_manufacturer_phone(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Введите телефон поставщика:")
    await state.set_state(ManufacturerPhoneFindForm.GET_FIND)


async def get_customer_email(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Введите почту покупателя:")
    await state.set_state(CustomerEmailFindForm.GET_FIND)


async def get_customer_phone(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Введите телефон покупателя:")
    await state.set_state(CustomerPhoneFindForm.GET_FIND)


async def manufacturer_email_find(message: Message, state: FSMContext):
    title = 'manufacturer'
    param = 'email'
    answer = 'Поставщик с такой почтой не найден!'
    await get_find(message, state, title, param, answer)


async def manufacturer_phone_find(message: Message, state: FSMContext):
    title = 'manufacturer'
    param = 'phone'
    answer = 'Поставщик с таким телефоном не найден!'
    await get_find(message, state, title, param, answer)


async def customer_email_find(message: Message, state: FSMContext):
    title = 'customer'
    param = 'email'
    answer = 'Покупатель с такой почтой не найден!'
    await get_find(message, state, title, param, answer)


async def customer_phone_find(message: Message, state: FSMContext):
    title = 'customer'
    param = 'phone'
    answer = 'Покупатель с таким телефоном не найден!'
    await get_find(message, state, title, param, answer)
