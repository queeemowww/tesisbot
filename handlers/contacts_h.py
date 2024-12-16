from aiogram import types, Router
from aiogram import F

router = Router()

@router.callback_query(F.data == "contacts")
async def send_contacts(callback: types.CallbackQuery):
    await callback.message.answer('*Филиал в Санкт\-Петербурге:*\n🏢Грузовой Терминал Пулково, Пулковское шоссе, д37к4, правое крыло здания, 1 этаж, офис 1\.088\n🕘Режим работы: 9:00\-18:00\n📞\+79818401424\n📧expedia@tesis\.su')