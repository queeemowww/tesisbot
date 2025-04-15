from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

menu_builder = InlineKeyboardBuilder()
air_order_btn = types.InlineKeyboardButton(
    text="Заказать авиадоставку ✈️",
    callback_data="order")

fesco_btn = types.InlineKeyboardButton(
    text="Fesco RailJET 🚄",
    callback_data="fesco")

track_btn = types.InlineKeyboardButton(
    text="Трекинг 🔎",
    callback_data="track")

my_cargo_btn = types.InlineKeyboardButton(
    text="Мои грузы 📦",
    callback_data="mycargo")

contacts_btn = types.InlineKeyboardButton(
    text="Контакты 📍",
    callback_data="contacts")

operator_btn = types.InlineKeyboardButton(
    text="Оператор 👨‍💼",
    callback_data="manager")

menu_builder.row(air_order_btn)
menu_builder.row(fesco_btn)
menu_builder.row(my_cargo_btn, track_btn)
menu_builder.row(contacts_btn, operator_btn)