from aiogram import types, Router
from aiogram import F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
import states
from kb import manager_builder

router = Router()

@router.callback_query(F.data == "manager")
async def connect_manager(callback: types.CallbackQuery):
    await callback.message.answer("Опишите Ваш запрос оператору")
    await callback.message.bot.send_contact(chat_id=callback.message.chat.id, phone_number='+79818401424', first_name='Tesis operator')
