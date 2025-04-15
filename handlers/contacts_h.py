from aiogram import types, Router
from aiogram import F
from text import led_lat, led_lon
from aiogram.filters import Command
from aiogram.enums import ParseMode
from kb.menu_kb import menu_builder
from database.db import Db
from database.db_provider import set_db_instance

router = Router()

@router.callback_query(F.data == "contacts")
async def send_contacts(callback: types.CallbackQuery):
    try:
        database = Db()
        await database.init()
        set_db_instance(database)
        await callback.message.delete()
        await callback.message.answer('*Филиал в Санкт\-Петербурге:*\n🏢Грузовой Терминал Пулково, Пулковское шоссе, д37к4, правое крыло здания, 1 этаж, офис 1\.088\n🕘Режим работы: 9:00\-18:00\n📞\+79818401424\n📧expedia@tesis\.su')
        await callback.message.bot.send_location(callback.message.chat.id, led_lat, led_lon)
        await callback.message.answer('Выберите действие', reply_markup=menu_builder.as_markup())
    except:
        pass

@router.message(F.text.lower() == 'нюся')
async def send_nused(message: types.Message):
    await message.answer('💗💗💗💗💗💗💗💗💗💗💗💗💗💗💗💗💗💗💗💗💗💗💗💗')