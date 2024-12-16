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
    text="Связь с менеджером 👨‍💼",
    callback_data="manager"),
    width=1
    )

cancel_track_btn = types.InlineKeyboardButton(
    text = 'Отменить ❌',
    callback_data='cancel_tracking'
)

airport_track_builder = InlineKeyboardBuilder()
airport_track_builder.row(types.InlineKeyboardButton(
    text = "Пулково 🇱🇪🇩",
    callback_data='LED'),
    width=1
    )
airport_track_builder.row(
        cancel_track_btn
        )

tracking_cancel_builder = InlineKeyboardBuilder()
tracking_cancel_builder.add(
    cancel_track_btn
)

manager_builder = InlineKeyboardBuilder()
manager_builder.add(types.InlineKeyboardButton(
    text='Заверщить разговор ❌',
    callback_data='stop_manager'
    )
)