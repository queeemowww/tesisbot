from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from datetime import date
# order_departure_builder = ReplyKeyboardBuilder()
# order_departure_builder.add(types.KeyboardButton(
#     text = "Пулково LED 🇷🇺")
# )

# order_departure_builder.add(types.KeyboardButton(
#     text = "Внуково VKO 🇷🇺")
# )

# order_departure_builder.add(types.KeyboardButton(
#     text = "Шереметьево SVO 🇷🇺")
# )

# order_departure_builder.add(types.KeyboardButton(
#     text = "Домодедово DME 🇷🇺")
# )
# order_departure_builder.adjust(1)

# order_pcs_builder = ReplyKeyboardBuilder()
# order_pcs_builder.add(types.KeyboardButton(
#     text = "1")
# )

# order_pcs_builder.add(types.KeyboardButton(
#     text = "5")
# )

# order_pcs_builder.add(types.KeyboardButton(
#     text = "10")
# )
# order_pcs_builder.adjust(3)

# order_weight_builder = ReplyKeyboardBuilder()
# order_weight_builder.add(types.KeyboardButton(
#     text = "5")
# )

# order_weight_builder.add(types.KeyboardButton(
#     text = "25")
# )

# order_weight_builder.add(types.KeyboardButton(
#     text = "50")
# )
# order_weight_builder.adjust(3)

# order_vol_builder = ReplyKeyboardBuilder()
# order_vol_builder.add(types.KeyboardButton(
#     text = "0.05")
# )

# order_vol_builder.add(types.KeyboardButton(
#     text = "0.1")
# )

# order_vol_builder.add(types.KeyboardButton(
#     text = "0.5")
# )
# order_vol_builder.adjust(3)

order_time_builder = ReplyKeyboardBuilder()
order_time_builder.adjust(1)

# order_departure_builder = ReplyKeyboardBuilder()
# order_destination_builder = ReplyKeyboardBuilder()
# order_pieces_builder = ReplyKeyboardBuilder()
# order_weight_builder = ReplyKeyboardBuilder()
# order_volume_builder = ReplyKeyboardBuilder()
# order_shipper_name_builder = ReplyKeyboardBuilder()
# order_shipper_phone_builder = ReplyKeyboardBuilder()
# order_consignee_name_builder = ReplyKeyboardBuilder()
# order_consignee_phone_builder = ReplyKeyboardBuilder()

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
