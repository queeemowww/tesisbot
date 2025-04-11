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

tracker = {}
todelete = {}
router = Router()
tracks = {}
blank = {}
number = {}
airport = {}

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
    airport[callback.message.chat.id] = callback.data
    todelete[callback.message.chat.id] = await callback.message.answer_photo(photo = awb_blank, caption = 'Введите бланк ГАН \(первые три цифры, например\: *555*\-\.\.\.\.\.\)', 
                                  reply_markup= tracking_cancel_builder.as_markup())
    await state.set_state(states.Track.blank)

@router.callback_query(F.data == "SVO", states.Track.airport)
async def track_2_1(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    airport[callback.message.chat.id] = callback.data
    todelete[callback.message.chat.id] = await callback.message.answer_photo(photo = awb_blank, caption = 'Введите бланк ГАН \(первые три цифры, например\: *555*\-\.\.\.\.\.\)', 
                                  reply_markup= tracking_cancel_builder.as_markup())
    await state.set_state(states.Track.blank)

@router.message(states.Track.blank, F.text.len() == 3)
async def track_3(message: types.Message, state: FSMContext):
    blank[message.chat.id] = message.text
    await message.delete()
    await todelete[message.chat.id].delete()
    del todelete[message.chat.id]
    todelete[message.chat.id] = await message.answer_photo(photo = awb_num, caption = 'Введите номер ГАН \(8 цифр, например\: \.\.\.\-*12345678*\)', 
                                  reply_markup= tracking_cancel_builder.as_markup())
    await state.set_state(states.Track.number)

@router.message(states.Track.number, F.text.len() == 8)
async def track_4(message: types.Message, state: FSMContext):
    number[message.chat.id] = message.text
    await todelete[message.chat.id].delete()
    del todelete[message.chat.id]
    await message.delete()
    await state.set_state(None)
    todelete[message.chat.id] = await message.answer("Проверяю статус груза\. Пожалуйста, ожидайте")
    tracker[message.chat.id] = Tracker()

    match airport[message.chat.id]:
        case 'LED':
            tracks[message.chat.id] = await tracker[message.chat.id].track_led(blank[message.chat.id] + '-' + number[message.chat.id])
        case 'SVO':
            tracks[message.chat.id] = await tracker[message.chat.id].track_svo(blank[message.chat.id] + '-' + number[message.chat.id])
    try:
        await message.answer(tracks[message.chat.id], ParseMode.HTML, reply_markup=menu_builder.as_markup())
    except Exception as e:
        await message.answer('Не удалось найти накладную с номером ' + '<code>' + blank[message.chat.id] + '-' + number[message.chat.id] + '</code>', ParseMode.HTML, reply_markup=menu_builder.as_markup())
    await todelete[message.chat.id].delete()
    del blank[message.chat.id]
    del number[message.chat.id]
    del tracker[message.chat.id]
    del tracks[message.chat.id]

@router.callback_query(F.data == 'cancel_tracking', StateFilter(states.Track))
async def cancel_track(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer('<i>Трекинг отменен</i>', reply_markup=menu_builder.as_markup(), parse_mode=ParseMode.HTML)
    await state.set_state(None)

@router.message(states.Track.blank)
async def track_2_incorrect(message: types.Message):
    await todelete[message.chat.id].delete()
    del todelete[message.chat.id]
    todelete[message.chat.id] = await message.answer('Введите *правильный* бланк ГАН \(первые три цифры, например\: *555*\-\.\.\.\.\.\)', 
                         reply_markup= tracking_cancel_builder.as_markup())
    await message.delete()

@router.message(states.Track.number)
async def track_3_incorrect(message: types.Message):
    await todelete[message.chat.id].delete()
    del todelete[message.chat.id]
    todelete[message.chat.id] = await message.answer('Введите *правильный* номер ГАН \(8 цифр, например\: \.\.\.\-*12345678*\)', 
                         reply_markup= tracking_cancel_builder.as_markup())
    await message.delete()


