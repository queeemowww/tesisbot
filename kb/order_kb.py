from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from datetime import date

# def kb_builder(message: types.Message, departure_builder, dest):
#     departure_builder[message.chat.id] = ReplyKeyboardBuilder()
#     destination_builder[message.chat.id] = ReplyKeyboardBuilder()
#     pieces_builder[message.chat.id] = ReplyKeyboardBuilder()
#     weight_builder[message.chat.id] = ReplyKeyboardBuilder()
#     volume_builder[message.chat.id] = ReplyKeyboardBuilder()
#     shipper_name_builder[message.chat.id] = ReplyKeyboardBuilder()
#     shipper_phone_builder[message.chat.id] = ReplyKeyboardBuilder()
#     consignee_name_builder[message.chat.id] = ReplyKeyboardBuilder()
#     consignee_phone_builder[message.chat.id] = ReplyKeyboardBuilder()

departure_buttons = []
departure_buttons.append(types.KeyboardButton(
    text = "Пулково LED 🇷🇺")
)

departure_buttons.append(types.KeyboardButton(
    text = "Внуково VKO 🇷🇺")
)

departure_buttons.append(types.KeyboardButton(
    text = "Шереметьево SVO 🇷🇺")
)

destination_buttons = []
destination_buttons.append(types.KeyboardButton(
    text = "Пулково LED 🇷🇺")
)

destination_buttons.append(types.KeyboardButton(
    text = "Внуково VKO 🇷🇺")
)

destination_buttons.append(types.KeyboardButton(
    text = "Шереметьево SVO 🇷🇺")
)

pieces_buttons = []
pieces_buttons.append(types.KeyboardButton(
    text = "1")
)

pieces_buttons.append(types.KeyboardButton(
    text = "5")
)

pieces_buttons.append(types.KeyboardButton(
    text = "10")
)

weight_buttons = []
weight_buttons.append(types.KeyboardButton(
    text = "5")
)

weight_buttons.append(types.KeyboardButton(
    text = "25")
)

weight_buttons.append(types.KeyboardButton(
    text = "50")
)

volume_buttons = []
volume_buttons.append(types.KeyboardButton(
    text = "0.05")
)

volume_buttons.append(types.KeyboardButton(
    text = "0.1")
)

volume_buttons.append(types.KeyboardButton(
    text = "0.5")
)

shipper_name_buttons = []
shipper_phone_buttons = []
consignee_name_buttons = []
consignee_phone_buttons = []

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
    width=3
)

order_change_builder.row(types.InlineKeyboardButton(
    text = "Изменить🔄",
    callback_data='change'),
    width=3
)

order_change_builder.row(types.InlineKeyboardButton(
    text = "Отменить❌",
    callback_data='cancel'),
    width=3
)

order_send_builder = InlineKeyboardBuilder()
order_send_builder.row(types.InlineKeyboardButton(
    text = "Отправить✅",
    callback_data='send'),
    width=2
)

order_send_builder.row(types.InlineKeyboardButton(
    text = "Отменить❌",
    callback_data='cancel'),
    width=2
)
