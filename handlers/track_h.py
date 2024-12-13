from aiogram import types, Router
from aiogram import F
from kb import airport_track_builder
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
import states

from utils.tarcker import Tracker

router = Router()

@router.callback_query(F.data == "track", StateFilter(None))
async def track_1(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('Выберите аэропорт отправления',
                                reply_markup=airport_track_builder.as_markup())
    await state.set_state(states.Track.airport)

@router.callback_query(F.data == "LED", states.Track.airport)
async def track_2(callback: types.Message, state: FSMContext):
    print('track2')
    global airport
    airport = F.data
    await callback.message.answer('Введите бланк ГАН \(первые три цифры, например\: *555*\-\.\.\.\.\.\)')
    await state.set_state(states.Track.blank)

@router.message(states.Track.blank, F.text.len() == 3)
async def track_3(message: types.Message, state: FSMContext):
    global blank
    blank = message.text
    print(type(message.text))
    await message.answer('Введите номер ГАН \(8 цифр, например\: \.\.\.\-*12345678*\)')
    await state.set_state(states.Track.number)

@router.message(states.Track.number, F.text.len() == 8)
async def track_4(message: types.message, state: FSMContext):
    global number
    number = message.text
    print(type(message.text))
    await state.set_state(None)
    tracker = Tracker(blank, number, airport)
    states = await tracker.track_led()
    await message.answer(states, ParseMode.HTML)

@router.message(states.Track.blank)
async def track_2_incorrect(message: types.Message):
    await message.answer('Введите *правильный* бланк ГАН \(первые три цифры, например\: *555*\-\.\.\.\.\.\)')

@router.message(states.Track.number)
async def track_3_incorrect(message: types.Message):
    await message.answer('Введите *правильный* номер ГАН \(8 цифр, например\: \.\.\.\-*12345678*\)')


