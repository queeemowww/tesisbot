
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command, StateFilter
from aiogram import F
from kb import menu_builder, airport_track_builder
from aiogram.fsm.context import FSMContext
from kb import order_departure_builder
from states import Order
from aiogram.enums import ParseMode
from admin import admin_ids
router = Router()

admin_id = admin_ids['Gleb']

@router.callback_query(F.data == "order", StateFilter(None))
async def order_1(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('Заполните поля (нажмите, чтобы скопировать):\n<code>1. Аэропорт отправления:\n2. Аэропорт прибытия:\n3. Характер груза (краткое описание груза):\n4. Количество мест:\n5. Общий вес:\n6. Общий объем:\n7. ФИО отправителя:\n Контактный номер отправителя:\n8. ФИО получателя\n Контактный номер получателя:\n</code>', parse_mode=ParseMode.HTML)
    await state.set_state(Order.to)

@router.message(StateFilter(Order.to))
async def order_2(message: types.Message, state: FSMContext):
    await message.bot.forward_message(admin_ids['Gleb'], message.chat.id, message.message_id)
    await message.reply('Заявка успешно отправлена\! Наш сотрудник свяжется с Вами в рабочее время')
    await state.set_state(None)
