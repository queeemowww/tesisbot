from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

menu_builder = InlineKeyboardBuilder()
menu_builder.add(types.InlineKeyboardButton(
    text="Оформить заказ",
    callback_data="order")
    )
menu_builder.add(types.InlineKeyboardButton(
    text="Трекинг груза",
    callback_data="track")
    )
menu_builder.add(types.InlineKeyboardButton(
    text="Контакты",
    callback_data="contacts")
    )
menu_builder.add(types.InlineKeyboardButton(
    text="Связь с менеджером",
    callback_data="manager")
    )

airport_track_builder = InlineKeyboardBuilder()
airport_track_builder.add(types.InlineKeyboardButton(
    text = "Пулково LED",
    callback_data='LED')
    )