
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

manager_builder = InlineKeyboardBuilder()
manager_builder.add(types.InlineKeyboardButton(
    text='Заверщить разговор ❌',
    callback_data='stop_manager')
    )