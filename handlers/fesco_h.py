from aiogram import types, Router
from aiogram.types import ReplyKeyboardRemove
from aiogram.filters import Command, StateFilter
from aiogram import F
from aiogram.fsm.context import FSMContext
from kb.order_kb import  order_change_builder, order_phone_builder, order_time_builder, order_send_builder
from kb.order_kb import departure_buttons, destination_buttons, pieces_buttons, weight_buttons, volume_buttons
from kb.order_kb import shipper_name_buttons, shipper_phone_buttons, consignee_name_buttons, consignee_phone_buttons, get_change_awb
from kb.menu_kb import menu_builder
from states import Order
from aiogram.enums import ParseMode
from admin import admin_ids
from database.db_provider import get_db, set_db_instance
from database.db import Db
router = Router()
import datetime
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from utils.email_send import Send_order


@router.callback_query(F.data == "fesco", StateFilter(None))
async def fesco_1(callback: types.CallbackQuery, state: FSMContext):
    try:
        database = Db()
        await database.init()
        set_db_instance(database)
        await callback.message.delete()
        await callback.message.answer('''<b>RAIL JET</b> — это регулярные импортные и экспортные отправки грузов в багажных вагонах, которые следуют в составе пассажирских поездов по ключевым маршрутам:
<code>📍Хуньчунь (КНР) – Москва (Ярославский вокзал)
📍Москва (Ярославский вокзал) – Хуньчунь (КНР)</code>
Наши поезда, состоящие из 16 багажных вагонов, курсируют <b>до трех раз в неделю</b>, обеспечивая бесперебойную логистику для вашего бизнеса''', reply_markup=menu_builder.as_markup(), parse_mode=ParseMode.HTML)
    except:
        pass
    finally:
        await database.close()
