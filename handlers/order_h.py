
from aiogram import types, Router
from aiogram.types import ReplyKeyboardRemove
from aiogram.filters import Command, StateFilter
from aiogram import F
from aiogram.fsm.context import FSMContext
from kb.order_kb import order_departure_builder, order_change_builder, order_pcs_builder, order_phone_builder
from kb.order_kb import order_weight_builder, order_vol_builder, order_time_builder, order_fio_builder
from states import Order
from aiogram.enums import ParseMode
from admin import admin_ids
router = Router()
import datetime
from aiogram.utils.keyboard import ReplyKeyboardBuilder

admin_id = admin_ids['Gleb']

order = {}

@router.callback_query(F.data == "order", StateFilter(None))
async def order_1(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('1/10 \- Введите аэропорт/город *отправления*', reply_markup=order_departure_builder.as_markup())
    await state.set_state(Order.departure)

@router.message(StateFilter(Order.departure))
async def order_2(message: types.Message, state: FSMContext):
    await message.answer('<code>Аэропорт/город *отправления*: ' + message.text+ "</code>", reply_markup=order_change_builder.as_markup(), parse_mode=ParseMode.HTML)
    order['Аэропорт/город отправления'] = message.text

@router.callback_query(F.data == "change", StateFilter(Order.departure))
async def order_3(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('1/10 \- Введите аэропорт/город *отправления*', reply_markup=order_departure_builder.as_markup())

@router.callback_query(F.data == "continue", StateFilter(Order.departure))
async def order4(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('2/10 \- Введите аэропорт/город *прибытия*', reply_markup=order_departure_builder.as_markup())
    await state.set_state(Order.to)

@router.message(StateFilter(Order.to))
async def order_5(message: types.Message, state: FSMContext):
    await message.answer('<code>Аэропорт/город прибытия: ' + message.text+ "</code>", reply_markup=order_change_builder.as_markup(), parse_mode=ParseMode.HTML)
    order['Аэропорт/город прибытия'] = message.text

@router.callback_query(F.data == "change", StateFilter(Order.to))
async def order_6(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('2/10 \- Введите аэропорт/город *прибытия*', reply_markup=order_departure_builder.as_markup())

@router.callback_query(F.data == "continue", StateFilter(Order.to))
async def order7(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('3/10 \- Введите *количество мест*:', reply_markup=order_pcs_builder.as_markup())
    await state.set_state(Order.pcs)

@router.message(StateFilter(Order.pcs))
async def order8(message: types.Message, state: FSMContext):
    order['Количество мест'] = message.text
    await message.answer('<code>Количество мест: ' + message.text+ "</code>", reply_markup=order_change_builder.as_markup(), parse_mode=ParseMode.HTML)

@router.callback_query(F.data == "change", StateFilter(Order.pcs))
async def order_9(callback: types.CallbackQuery, state: FSMContext):
     await callback.message.answer('3/10 \- Введите *количество мест*:', reply_markup=order_pcs_builder.as_markup())

@router.callback_query(F.data == "continue", StateFilter(Order.pcs),)
async def order10(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('4/10 \- Введите <b>общий вес груза(кг)</b>:', reply_markup=order_weight_builder.as_markup(), parse_mode=ParseMode.HTML)
    await state.set_state(Order.weight)
    print(order)

@router.message(StateFilter(Order.weight))
async def order11(message: types.Message, state: FSMContext):
    await message.answer('<code>Общий вес груза(кг): ' + message.text+ "</code>", reply_markup=order_change_builder.as_markup(), parse_mode=ParseMode.HTML)
    order['Общий вес груза'] = message.text

@router.callback_query(F.data == "change", StateFilter(Order.weight))
async def order_12(callback: types.CallbackQuery, state: FSMContext):
     await callback.message.answer('4/10 \- Введите <b>общий вес груза(кг)</b>:', reply_markup=order_weight_builder.as_markup(), parse_mode=ParseMode.HTML)

@router.callback_query(F.data == "continue", StateFilter(Order.weight))
async def order13(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('5/10 - Введите <b>общий объем груза(куб. м)</b>:', reply_markup=order_vol_builder.as_markup(),parse_mode=ParseMode.HTML)
    await state.set_state(Order.vol)

@router.message(StateFilter(Order.vol))
async def order12(message: types.Message, state: FSMContext):
    await message.answer('<code>Общий объем груза(куб. м): ' + message.text+ "</code>", reply_markup=order_change_builder.as_markup(), parse_mode=ParseMode.HTML)
    order['Общий объем груза'] = message.text
    
@router.callback_query(F.data == "change", StateFilter(Order.vol))
async def order_13(callback: types.CallbackQuery, state: FSMContext):
     await callback.message.answer('5/10 - Введите <b>общий объем груза(куб. м)</b>:', reply_markup=order_vol_builder.as_markup(), parse_mode=ParseMode.HTML)

@router.callback_query(F.data == "continue", StateFilter(Order.vol))
async def order14(callback: types.CallbackQuery, state: FSMContext):
    get_time()
    await callback.message.answer('6/10 \- Введите *дату привоза груза на склад*:', reply_markup=order_time_builder.as_markup())
    remove_time()
    await state.set_state(Order.planned_time)

@router.message(StateFilter(Order.planned_time))
async def order15(message: types.Message, state: FSMContext):
    await message.answer('<code>Дата привоза груза на склад: ' + message.text+ "</code>", reply_markup=order_change_builder.as_markup(), parse_mode=ParseMode.HTML)
    order['Планируемая дата привоза на склад'] = message.text

@router.callback_query(F.data == "change", StateFilter(Order.planned_time))
async def order_16(callback: types.CallbackQuery, state: FSMContext):
    get_time()
    await callback.message.answer('6/10 \- Введите *дату привоза груза на склад*:', reply_markup=order_time_builder.as_markup())
    remove_time()

@router.callback_query(F.data == "continue", StateFilter(Order.planned_time))
async def order17(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('7/10 \- Введите *ФИО/Название организации отправителя*', reply_markup=ReplyKeyboardRemove())
    await state.set_state(Order.shipper_name)

@router.message(StateFilter(Order.shipper_name))
async def order18(message: types.Message, state: FSMContext):
    order['ФИО/Название организации отправителя'] = message.text
    await message.answer('<code>ФИО/Название организации отправителя: ' + message.text+ "</code>", parse_mode=ParseMode.HTML, reply_markup=order_change_builder.as_markup())

@router.callback_query(F.data == "change", StateFilter(Order.shipper_name))
async def order_19(callback: types.CallbackQuery, state: FSMContext):
     await callback.message.answer('7/10 \- Введите *ФИО/Название организации отправителя*:', reply_markup=order_time_builder.as_markup())

@router.callback_query(F.data == "continue", StateFilter(Order.shipper_name))
async def order20(callback: types.CallbackQuery, state: FSMContext):
    get_phone()
    await callback.message.answer('8/10 \- Введите *номер телефона отправителя*', reply_markup=order_phone_builder.as_markup())
    remove_phone()
    await state.set_state(Order.shipper_num)

@router.message(StateFilter(Order.shipper_num), F.text)
async def order21(message: types.Message, state: FSMContext):
    order['Номер телефона отправителя'] = message.text
    await message.answer('<code>Номер телефона отправителя: ' + message.text+ "</code>", parse_mode=ParseMode.HTML, reply_markup=order_change_builder.as_markup())

@router.message(StateFilter(Order.shipper_num), F.contact)
async def order21_1(message: types.Message, state: FSMContext):
    order['Номер телефона отправителя'] = message.contact.phone_number
    await message.answer('<code>Номер телефона отправителя: ' + message.contact.phone_number+ "</code>", parse_mode=ParseMode.HTML, reply_markup=order_change_builder.as_markup())

@router.callback_query(F.data == "change", StateFilter(Order.shipper_num))
async def order_22(callback: types.CallbackQuery, state: FSMContext):
     get_phone()
     await callback.message.answer('8/10 \- Введите *номер телефона отправителя*:')
     remove_phone()

@router.callback_query(F.data == "continue", StateFilter(Order.shipper_num))
async def order23(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('9/10 \- Введите *ФИО/Название организации получателя*', reply_markup=ReplyKeyboardRemove())
    await state.set_state(Order.consignee_name)

@router.message(StateFilter(Order.consignee_name))
async def order24(message: types.Message, state: FSMContext):
    order['ФИО/Название организации получателя'] = message.text
    await message.answer('<code>ФИО/Название организации получателя: ' + message.text+ "</code>", parse_mode=ParseMode.HTML, reply_markup=order_change_builder.as_markup())

@router.callback_query(F.data == "change", StateFilter(Order.consignee_name))
async def order_25(callback: types.CallbackQuery, state: FSMContext):
     await callback.message.answer('9/10 \- Введите *ФИО/Название организации получателя*:')

@router.callback_query(F.data == "continue", StateFilter(Order.consignee_name))
async def order26(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('10/10 \- Введите *номер телефона получателя*:', reply_markup=ReplyKeyboardRemove())
    await state.set_state(Order.consignee_num)

@router.message(StateFilter(Order.consignee_num))
async def order27(message: types.Message, state: FSMContext):
    order['Номер телефона получателя'] = message.text
    await message.answer('<code>Номер телефона получателя: ' + message.text+ "</code>", parse_mode=ParseMode.HTML, reply_markup=order_change_builder.as_markup())

@router.callback_query(F.data == "change", StateFilter(Order.consignee_num))
async def order_28(callback: types.CallbackQuery, state: FSMContext):
     await callback.message.answer('10/10 \- Введите *номер телефона полцчателя*:')

@router.callback_query(F.data == "continue", StateFilter(Order.consignee_num))
async def order_check(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('Проверьте корректность запроса:\n' + '<code>1 - Аэропорт/город отправления: ' + order['Аэропорт/город отправления'] +
                                  '\n2 - Аэропорт/город прибытия: ' + order['Аэропорт/город прибытия'] +
                                  '\n3 - Количество мест: ' + order['Количество мест'] +
                                  '\n4 - Общий вес груза: ' + order['Общий вес груза'] +
                                  '\n5 - Общий объем груза: ' + order['Общий объем груза'] +
                                  '\n6 - Планируемая дата привоза на склад: ' + order['Планируемая дата привоза на склад'] +
                                  '\n7 - ФИО/Название организации отправителя: ' + order['ФИО/Название организации отправителя'] +
                                  '\n8 - Номер телефона отправителя: ' + order['Номер телефона отправителя'] +
                                  '\n9 - ФИО/Название организации получвтеля: ' + order['ФИО/Название организации получателя'] +
                                  '\n10 - Номер телефона получателя: ' + order['Номер телефона получателя'] + '</code>', 
                                  reply_markup=types.ReplyKeyboardRemove(), parse_mode=ParseMode.HTML
    )
    await state.set_state(Order.send)

@router.message(StateFilter(Order.send))
async def order_send(message: types.Message, state: FSMContext):
    mes = '<code>1 - Аэропорт/город отправления: ' + order['Аэропорт/город отправления'] +'\n2 - Аэропорт/город прибытия: ' + order['Аэропорт/город прибытия'] +'\n3 - Количество мест: ' + order['Количество мест'] +'\n4 - Общий вес груза: ' + order['Общий вес груза'] +'\n5 - Общий объем груза: ' + order['Общий объем груза'] +'\n6 - Планируемая дата привоза на склад: ' + order['Планируемая дата привоза на склад'] +'\n7 - ФИО/Название организации отправителя: ' + order['ФИО/Название организации отправителя'] +'\n8 - Номер телефона отправителя: ' + order['Номер телефона отправителя'] +'\n9 - ФИО/Название организации получвтеля: ' + order['ФИО/Название организации получателя'] +'\n10 - Номер телефона получателя: ' + order['Номер телефона получателя'] + '</code>'
    await message.bot.send_message(chat_id=admin_ids['Gleb'], text = mes, parse_mode=ParseMode.HTML)
    await message.reply('Заявка успешно отправлена\! Наш сотрудник свяжется с Вами в рабочее время')
    await state.set_state(None)

@router.callback_query(F.data == "cancel")
async def order_cancel(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('Заявка отменена', reply_markup=ReplyKeyboardRemove())
    await state.set_state(None)

def get_phone():
    order_phone_builder.add(types.KeyboardButton(
        text="Отправить номер телефона",
        request_contact=True
    )
    )

def remove_phone():
    order_phone_builder = ReplyKeyboardBuilder()

def get_time():
    order_time_builder.add(types.KeyboardButton(
    text = datetime.date.today().strftime('%d-%m-%y') 
    )
    )

    order_time_builder.add(types.KeyboardButton(
    text = (datetime.date.today() + datetime.timedelta(days=1)).strftime('%d-%m-%y') 
    )
    )

    order_time_builder.add(types.KeyboardButton(
    text = (datetime.date.today() + datetime.timedelta(days=5)).strftime('%d-%m-%y') 
    )
    )

def remove_time():
    order_time_builder = ReplyKeyboardBuilder()