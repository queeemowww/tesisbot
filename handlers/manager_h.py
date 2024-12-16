from aiogram import types, Router
from aiogram import F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
import states
from kb import manager_builder


router = Router()


@router.callback_query(F.data == "manager")
async def connect_manager(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('Переключаю на менеджера\.\.\.', reply_markup=manager_builder.as_markup())
    await state.set_state(states.Manager.manager)

# @router.message(states.Manager.manager)
# async def send_to_manager(message: types.Message, state: FSMContext):
#     await bot.send_message

@router.callback_query(states.Manager.manager, F.data == 'stop_manager')
async def manager_2(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('Конец разговора с менеджером')
    await state.set_state(None)