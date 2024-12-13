
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command, StateFilter
from aiogram import F
from kb import menu_builder, airport_track_builder

router = Router()

@router.callback_query(F.data == "order")
async def make_order(callback: types.CallbackQuery):
    await callback.message.answer('Заполните поля')

@router.callback_query(F.data == "contacts")
async def send_contacts(callback: types.CallbackQuery):
    await callback.message.answer('Филиал в Санкт\-Петербурге:\nГрузовой Терминал Пулково, *Пулковское шоссе, д37к4, правое крыло здания, 1 этаж, офис 1\.088*\nРежим работы: *9:00\-18:00*\n*\+79253264321*')

@router.callback_query(F.data == "manager")
async def connect_manager(callback: types.CallbackQuery):
    await callback.message.answer('Переключаю на менеджера\.\.\.')

@router.message(F.text, StateFilter(None))
async def all_msgs(message: types.Message):
    await message.answer("слыш бля")
