from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from datetime import date
order_departure_builder = ReplyKeyboardBuilder()
order_departure_builder.add(types.KeyboardButton(
    text = "Пулково 🇱🇪🇩")
)

order_departure_builder.add(types.KeyboardButton(
    text = "Внуково 🇱🇪🇩")
)

order_departure_builder.add(types.KeyboardButton(
    text = "Шереметьево 🇱🇪🇩")
)

order_departure_builder.add(types.KeyboardButton(
    text = "Домодедово 🇱🇪🇩")
)
order_departure_builder.adjust(1)

order_pcs_builder = ReplyKeyboardBuilder()
order_pcs_builder.add(types.KeyboardButton(
    text = "1")
)

order_pcs_builder.add(types.KeyboardButton(
    text = "5")
)

order_pcs_builder.add(types.KeyboardButton(
    text = "10")
)
order_pcs_builder.adjust(3)

order_weight_builder = ReplyKeyboardBuilder()
order_weight_builder.add(types.KeyboardButton(
    text = "5")
)

order_weight_builder.add(types.KeyboardButton(
    text = "25")
)

order_weight_builder.add(types.KeyboardButton(
    text = "50")
)
order_weight_builder.adjust(3)

order_vol_builder = ReplyKeyboardBuilder()
order_vol_builder.add(types.KeyboardButton(
    text = "0.05")
)

order_vol_builder.add(types.KeyboardButton(
    text = "0.1")
)

order_vol_builder.add(types.KeyboardButton(
    text = "0.5")
)
order_vol_builder.adjust(3)

order_time_builder = ReplyKeyboardBuilder()
order_time_builder.adjust(1)

order_fio_builder = ReplyKeyboardBuilder()
order_fio_builder.adjust(1)

order_phone_builder = ReplyKeyboardBuilder()
order_phone_builder.adjust(1)

order_change_builder = InlineKeyboardBuilder()
order_change_builder.row(types.InlineKeyboardButton(
    text = "Продолжить✅",
    callback_data='continue'),
    width=1
)

order_change_builder.row(types.InlineKeyboardButton(
    text = "Изменить🔄",
    callback_data='change'),
    width=1
)

order_change_builder.row(types.InlineKeyboardButton(
    text = "Отменить❌",
    callback_data='cancel'),
    width=1
)

