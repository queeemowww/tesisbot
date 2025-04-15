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
prev = {}

@router.callback_query(F.data == "mycargo")
async def connect_manager(callback: types.CallbackQuery):
    try:
        database = Db()
        await database.init()
        set_db_instance(database)
        await callback.message.delete()
        prev[callback.message.chat.id] = await callback.message.answer('Мои грузы📦', reply_markup=menu_builder.as_markup())
    except:
        pass

