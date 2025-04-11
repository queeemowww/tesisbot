from aiogram import types, Router
from aiogram import F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
import states
from kb.manager_kb import manager_builder
from kb.menu_kb import menu_builder
from database.db import Db
from database.db_provider import set_db_instance


router = Router()

@router.callback_query(F.data == "manager")
async def connect_manager(callback: types.CallbackQuery):
    database = Db()
    await database.init()
    set_db_instance(database)
    await callback.message.delete()
    await callback.message.answer("Опишите Ваш запрос оператору")
    await callback.message.bot.send_contact(chat_id=callback.message.chat.id, phone_number='+79818401424', first_name='Tesis operator')
    await callback.message.answer('Выберите действие', reply_markup=menu_builder.as_markup())

