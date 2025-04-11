from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from database.db_provider import get_db
from datetime import date

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


async def get_change_awb(pcs, w, v, fr, dest, date, shipper_fio, shipper_phone, consignee_fio, consignee_phone):
    change_awb_builder = InlineKeyboardBuilder()
    close_btn = types.InlineKeyboardButton(
            text = '❌',
            callback_data='close')
    
    go_btn = types.InlineKeyboardButton(
            text = '✅',
            callback_data='go')
    
    pcs_btn = (types.InlineKeyboardButton(
            text = f'Мест: {pcs}',
            callback_data='pieces'
    ))

    weight_btn = (types.InlineKeyboardButton(
            text = f'Вес: {w}',
            callback_data='weight'
    ))

    vol_btn = (types.InlineKeyboardButton(
            text = f'Объем: {v}',
            callback_data='volume'
    ))

    # cargo_btn = (types.InlineKeyboardButton(
    #         text = f'Груз: {cargo}',
    #         callback_data='cargo'
    # ))

    fr_btn = (types.InlineKeyboardButton(
            text = f'Из: {fr}',
            callback_data='departure'
    ))

    dest_btn = (types.InlineKeyboardButton(
            text = f'До: {dest}',
            callback_data='destination'
    ))

    date_btn = (types.InlineKeyboardButton(
            text = f'Дата: {date}',
            callback_data='date'
    ))
    shipper_fio_btn = (types.InlineKeyboardButton(
            text = f'От: {shipper_fio}',
            callback_data='shfio'
    ))
    shipper_phone_btn = (types.InlineKeyboardButton(
            text = f'{shipper_phone}',
            callback_data='shphone'
    ))
    consignee_fio_btn = (types.InlineKeyboardButton(
            text = f'Пол: {consignee_fio}',
            callback_data='cnfio'
    ))
    consignee_phone_btn = (types.InlineKeyboardButton(
            text = f'{consignee_phone}',
            callback_data='cnphone'
    ))

    change_awb_builder.row(pcs_btn, weight_btn)
    change_awb_builder.row(vol_btn)
    change_awb_builder.row(fr_btn, dest_btn)
    change_awb_builder.row(shipper_fio_btn, shipper_phone_btn)
    change_awb_builder.row(consignee_fio_btn, consignee_phone_btn)
    change_awb_builder.row(close_btn, go_btn)

    return change_awb_builder.as_markup()
    