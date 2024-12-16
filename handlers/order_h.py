
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command, StateFilter
from aiogram import F
from kb import menu_builder, airport_track_builder

router = Router()

@router.callback_query(F.data == "order")
async def make_order(callback: types.CallbackQuery):
    await callback.message.answer('Заполните поля')

@router.message(F.text != '/track', StateFilter(None))
async def all_msgs(message: types.Message):
    await message.answer("Пожалуйста, выберите действие", reply_markup=menu_builder.as_markup())
