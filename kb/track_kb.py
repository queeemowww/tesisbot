from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

cancel_track_btn = types.InlineKeyboardButton(
    text = 'Отменить ❌',
    callback_data='cancel_tracking'
    )

airport_track_builder = InlineKeyboardBuilder()
airport_track_builder.row(types.InlineKeyboardButton(
    text = "Пулково LED 🇷🇺",
    callback_data='LED'),
    width=1
    )
airport_track_builder.row(types.InlineKeyboardButton(
    text = "Шереметьево SVO 🇷🇺",
    callback_data='SVO'),
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
    callback_data='stop_manager')
)


awb_blank_builder = ReplyKeyboardBuilder()

awb_blank_builder.add(types.KeyboardButton(
    text = "555"
)
)
awb_blank_builder.add(types.KeyboardButton(
    text = "421"
))

awb_blank_builder.add(types.KeyboardButton(
    text = "216"
))