from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

menu_builder = InlineKeyboardBuilder()
menu_builder.row(types.InlineKeyboardButton(
    text="Оформить заказ ✈️",
    callback_data="order"),
    width = 1
    )
menu_builder.row(types.InlineKeyboardButton(
    text="Трекинг груза 🔎",
    callback_data="track"),
    width = 1
    )
menu_builder.row(types.InlineKeyboardButton(
    text="Контакты 📍",
    callback_data="contacts"),
    width = 1
    )
menu_builder.row(types.InlineKeyboardButton(
    text="Связь с оператором 👨‍💼",
    callback_data="manager"),
    width=1
    )