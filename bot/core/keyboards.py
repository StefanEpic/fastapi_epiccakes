from aiogram.utils.keyboard import InlineKeyboardBuilder


def menu_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Авторизация', callback_data='login')
    keyboard_builder.button(text='Поставщик', callback_data='manufacturer')
    keyboard_builder.button(text='Покупатель', callback_data='customer')

    keyboard_builder.adjust(1, 2)
    return keyboard_builder.as_markup()


def manufacturer_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Почте', callback_data='m_email')
    keyboard_builder.button(text='Телефону', callback_data='m_phone')

    keyboard_builder.adjust(2)
    return keyboard_builder.as_markup()


def customer_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Почте!', callback_data='c_email')
    keyboard_builder.button(text='Телефону!', callback_data='c_phone')

    keyboard_builder.adjust(2)
    return keyboard_builder.as_markup()
