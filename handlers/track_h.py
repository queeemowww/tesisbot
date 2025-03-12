from aiogram import types, Router
from aiogram import F
from kb.track_kb import airport_track_builder,tracking_cancel_builder, awb_blank_builder
from kb.menu_kb import menu_builder
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
import states
from aiogram.types.input_file import FSInputFile

awb_blank = FSInputFile('./img/awb_blank.png')
awb_num = FSInputFile('./img/awb_num.png')

from utils.tarcker import Tracker

tracker = Tracker()
todelete = []
router = Router()

@router.callback_query(F.data == "track", StateFilter(None))
async def track_1(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer('Выберите аэропорт отправления',
                                reply_markup=airport_track_builder.as_markup())
    await state.set_state(states.Track.airport)

@router.message(StateFilter(None), Command('track'))
async def track_1_1(message: types.Message, state: FSMContext):
    await message.answer('Выберите аэропорт отправления',
                                reply_markup=airport_track_builder.as_markup())
    await state.set_state(states.Track.airport)

@router.callback_query(F.data == "LED", states.Track.airport)
async def track_2(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    global airport
    airport = callback.data
    a = await callback.message.answer_photo(photo = awb_blank, caption = 'Введите бланк ГАН \(первые три цифры, например\: *555*\-\.\.\.\.\.\)', 
                                  reply_markup= tracking_cancel_builder.as_markup())
    todelete.append(a)
    await state.set_state(states.Track.blank)

@router.message(states.Track.blank, F.text.len() == 3)
async def track_3(message: types.Message, state: FSMContext):
    global blank
    blank = message.text
    await message.delete()
    a = await message.answer_photo(photo = awb_num, caption = 'Введите номер ГАН \(8 цифр, например\: \.\.\.\-*12345678*\)', 
                                  reply_markup= tracking_cancel_builder.as_markup())
    await todelete[-1].delete()
    todelete.append(a)
    await state.set_state(states.Track.number)

@router.message(states.Track.number, F.text.len() == 8)
async def track_4(message: types.Message, state: FSMContext):
    global number
    number = message.text
    await todelete[-1].delete()
    await message.delete()
    await state.set_state(None)
    mes = await message.answer("Проверяю статус груза\. Пожалуйста, ожидайте")
    tracks = await tracker.track_led(blank, number, airport)
    await message.answer(tracks, ParseMode.HTML, reply_markup=menu_builder.as_markup())
    await mes.delete()

@router.callback_query(F.data == 'cancel_tracking', StateFilter(states.Track))
async def cancel_track(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer('<i>Трекинг отменен</i>', reply_markup=menu_builder.as_markup(), parse_mode=ParseMode.HTML)
    await state.set_state(None)

@router.message(states.Track.blank)
async def track_2_incorrect(message: types.Message):
    await todelete[-1].delete()
    a = await message.answer('Введите *правильный* бланк ГАН \(первые три цифры, например\: *555*\-\.\.\.\.\.\)', 
                         reply_markup= tracking_cancel_builder.as_markup())
    todelete.append(a)
    await message.delete()

@router.message(states.Track.number)
async def track_3_incorrect(message: types.Message):
    await todelete[-1].delete()
    a = await message.answer('Введите *правильный* номер ГАН \(8 цифр, например\: \.\.\.\-*12345678*\)', 
                         reply_markup= tracking_cancel_builder.as_markup())
    todelete.append(a)
    await message.delete()


