from aiogram import types, Router
from aiogram import F
from text import led_lat, led_lon
from aiogram.filters import Command

router = Router()

@router.callback_query(F.data == "contacts")
async def send_contacts(callback: types.CallbackQuery):
    await callback.message.answer('*Филиал в Санкт\-Петербурге:*\n🏢Грузовой Терминал Пулково, Пулковское шоссе, д37к4, правое крыло здания, 1 этаж, офис 1\.088\n🕘Режим работы: 9:00\-18:00\n📞\+79818401424\n📧expedia@tesis\.su')
    await callback.message.bot.send_location(callback.message.chat.id, led_lat, led_lon)

@router.message(F.text.lower() == 'нюся')
async def send_nused(message: types.Message):
    await message.answer('💗💗💗💗💗💗💗💗💗💗💗💗💗💗💗💗💗💗💗💗💗💗💗💗')