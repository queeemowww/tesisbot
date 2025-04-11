
from aiogram import types, Router
from aiogram.types import ReplyKeyboardRemove
from aiogram.filters import Command, StateFilter
from aiogram import F
from aiogram.fsm.context import FSMContext
from kb.order_kb import  order_change_builder, order_phone_builder, order_time_builder, order_send_builder
from kb.order_kb import departure_buttons, destination_buttons, pieces_buttons, weight_buttons, volume_buttons
from kb.order_kb import shipper_name_buttons, shipper_phone_buttons, consignee_name_buttons, consignee_phone_buttons
from kb.menu_kb import menu_builder
from states import Order
from aiogram.enums import ParseMode
from admin import admin_ids
from database.db_provider import get_db
router = Router()
import datetime
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from utils.email_send import Send_order

admin_id = admin_ids['Gleb']

order = {}
time_builder = {}
phone_builder = {}
prev = {}

@router.callback_query(F.data == "order", StateFilter(None))
async def order_1(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    order[callback.message.chat.id] = {}
    prev[callback.message.chat.id] = await callback.message.answer('1️⃣ \- *_Введите аэропорт/город отправления_*', reply_markup=get_previous_mrkp(callback.message.chat.id, 'departure'))
    await state.set_state(Order.departure)

@router.message(StateFilter(Order.departure))
async def order_2(message: types.Message, state: FSMContext):
    await prev[message.chat.id].delete()
    del prev[message.chat.id]
    await message.answer('Аэропорт/город отправления:<b> ' + message.text+ "</b>", reply_markup=order_change_builder.as_markup(), parse_mode=ParseMode.HTML)
    order[message.chat.id]['Аэропорт/город отправления'] = message.text
    await message.delete()

@router.callback_query(F.data == "change", StateFilter(Order.departure))
async def order_3(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    prev[callback.message.chat.id] = await callback.message.answer('1️⃣ \- *_Введите аэропорт/город отправления_*',reply_markup=get_previous_mrkp(callback.message.chat.id, 'departure'))

@router.callback_query(F.data == "continue", StateFilter(Order.departure))
async def order4(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    prev[callback.message.chat.id] = await callback.message.answer('2️⃣ \- *_Введите аэропорт/город прибытия_*',reply_markup=get_previous_mrkp(callback.message.chat.id, 'destination'))
    await state.set_state(Order.to)

@router.message(StateFilter(Order.to))
async def order_5(message: types.Message, state: FSMContext):
    await prev[message.chat.id].delete()
    del prev[message.chat.id]
    await message.answer('Аэропорт/город прибытия:<b> ' + message.text+ "</b>", reply_markup=order_change_builder.as_markup(), parse_mode=ParseMode.HTML)
    order[message.chat.id]['Аэропорт/город прибытия'] = message.text
    await message.delete()

@router.callback_query(F.data == "change", StateFilter(Order.to))
async def order_6(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    prev[callback.message.chat.id] = await callback.message.answer('2️⃣ \- *_Введите аэропорт/город прибытия_*', reply_markup=get_previous_mrkp(callback.message.chat.id, 'destination'))

@router.callback_query(F.data == "continue", StateFilter(Order.to))
async def order7(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    prev[callback.message.chat.id] = await callback.message.answer('3️⃣ \- *_Введите количество мест_*:', reply_markup=get_previous_mrkp(callback.message.chat.id, 'pieces'))
    await state.set_state(Order.pcs)

@router.message(StateFilter(Order.pcs))
async def order8(message: types.Message, state: FSMContext):
    await prev[message.chat.id].delete()
    del prev[message.chat.id]
    order[message.chat.id]['Количество мест'] = message.text
    await message.answer('Количество мест:<b> ' + message.text+ "</b>", reply_markup=order_change_builder.as_markup(), parse_mode=ParseMode.HTML)
    await message.delete()

@router.callback_query(F.data == "change", StateFilter(Order.pcs))
async def order_9(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    prev[callback.message.chat.id] = await callback.message.answer('4️⃣ \- *_Введите количество мест_*:', reply_markup=get_previous_mrkp(callback.message.chat.id, 'pieces'))

@router.callback_query(F.data == "continue", StateFilter(Order.pcs),)
async def order10(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    prev[callback.message.chat.id] = await callback.message.answer('4️⃣ - <b><i>Введите общий вес груза(кг)</i></b>:', reply_markup=get_previous_mrkp(callback.message.chat.id, 'weight'), parse_mode=ParseMode.HTML)
    await state.set_state(Order.weight)

@router.message(StateFilter(Order.weight))
async def order11(message: types.Message, state: FSMContext):
    await prev[message.chat.id].delete()
    del prev[message.chat.id]
    await message.answer('<code>Общий вес груза(кг): ' + message.text+ "</code>", reply_markup=order_change_builder.as_markup(), parse_mode=ParseMode.HTML)
    order[message.chat.id]['Общий вес груза'] = message.text
    await message.delete()

@router.callback_query(F.data == "change", StateFilter(Order.weight))
async def order_12(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    prev[callback.message.chat.id] = await callback.message.answer('4️⃣ - <b><i>Введите общий вес груза(кг)</i></b>:', reply_markup=get_previous_mrkp(callback.message.chat.id, 'weight'), parse_mode=ParseMode.HTML)

@router.callback_query(F.data == "continue", StateFilter(Order.weight))
async def order13(callback: types.CallbackQuery, state: FSMContext):
    prev[callback.message.chat.id] = await callback.message.answer('5️⃣ - <b><i>Введите общий объем груза(куб. м)</i></b>:', reply_markup=get_previous_mrkp(callback.message.chat.id, 'volume'),parse_mode=ParseMode.HTML)
    await state.set_state(Order.vol)
    await callback.message.delete()

@router.message(StateFilter(Order.vol))
async def order12(message: types.Message, state: FSMContext):
    await prev[message.chat.id].delete()
    del prev[message.chat.id]
    await message.answer('<code>Общий объем груза(куб. м): ' + message.text+ "</code>", reply_markup=order_change_builder.as_markup(), parse_mode=ParseMode.HTML)
    order[message.chat.id]['Общий объем груза'] = message.text
    await message.delete()

@router.callback_query(F.data == "change", StateFilter(Order.vol))
async def order_13(callback: types.CallbackQuery, state: FSMContext):
    prev[callback.message.chat.id] = await callback.message.answer('5️⃣- <b><i>Введите общий объем груза(куб. м)</i></b>:', reply_markup=get_previous_mrkp(callback.message.chat.id, 'volume'), parse_mode=ParseMode.HTML)
    await callback.message.delete()

@router.callback_query(F.data == "continue", StateFilter(Order.vol))
async def order14(callback: types.CallbackQuery, state: FSMContext):
    get_time(message=callback.message)
    prev[callback.message.chat.id] = await callback.message.answer('6️⃣\- *_Введите дату привоза груза на склад_*:', reply_markup=time_builder[callback.message.chat.id].as_markup(resize_keyboard = True))
    del time_builder[callback.message.chat.id]
    await state.set_state(Order.planned_time)
    await callback.message.delete()

@router.message(StateFilter(Order.planned_time))
async def order15(message: types.Message, state: FSMContext):
    await prev[message.chat.id].delete()
    del prev[message.chat.id]
    await message.answer('<code>Дата привоза груза на склад: ' + message.text+ "</code>", reply_markup=order_change_builder.as_markup(), parse_mode=ParseMode.HTML)
    order[message.chat.id]['Планируемая дата привоза на склад'] = message.text
    await message.delete()

@router.callback_query(F.data == "change", StateFilter(Order.planned_time))
async def order_16(callback: types.CallbackQuery, state: FSMContext):
    get_time(message=callback.message)
    prev[callback.message.chat.id] = await callback.message.answer('6️⃣ \- *_Введите дату привоза груза на склад_*:', reply_markup=time_builder[callback.message.chat.id].as_markup(resize_keyboard = True))
    del time_builder[callback.message.chat.id]
    await callback.message.delete()

@router.callback_query(F.data == "continue", StateFilter(Order.planned_time))
async def order17(callback: types.CallbackQuery, state: FSMContext):
    prev[callback.message.chat.id] = await callback.message.answer('7️⃣ \- *_Введите ФИО/Название организации отправителя_*', reply_markup=get_previous_mrkp(callback.message.chat.id, 'shipper_name'))
    await state.set_state(Order.shipper_name)
    await callback.message.delete()

@router.message(StateFilter(Order.shipper_name))
async def order18(message: types.Message, state: FSMContext):
    await prev[message.chat.id].delete()
    del prev[message.chat.id]
    order[message.chat.id]['ФИО/Название организации отправителя'] = message.text
    await message.answer('<code>ФИО/Название организации отправителя: ' + message.text+ "</code>", parse_mode=ParseMode.HTML, reply_markup=order_change_builder.as_markup())
    await message.delete()

@router.callback_query(F.data == "change", StateFilter(Order.shipper_name))
async def order_19(callback: types.CallbackQuery, state: FSMContext):
    prev[callback.message.chat.id] = await callback.message.answer('7️⃣ \- *_Введите ФИО/Название организации отправителя_*:', reply_markup=get_previous_mrkp(callback.message.chat.id, 'shipper_name'))
    await callback.message.delete()

@router.callback_query(F.data == "continue", StateFilter(Order.shipper_name))
async def order20(callback: types.CallbackQuery, state: FSMContext):
    # get_phone(message=callback.message)
    prev[callback.message.chat.id] = await callback.message.answer('8️⃣\- *_Введите номер телефона отправителя_*', reply_markup=get_previous_mrkp(callback.message.chat.id, 'shipper_phone'))
    # del phone_builder[callback.message.chat.id]
    await state.set_state(Order.shipper_num)
    await callback.message.delete()

@router.message(StateFilter(Order.shipper_num), F.text)
async def order21(message: types.Message, state: FSMContext):
    await prev[message.chat.id].delete()
    del prev[message.chat.id]
    order[message.chat.id]['Номер телефона отправителя'] = message.text
    await message.answer('<code>Номер телефона отправителя: ' + message.text+ "</code>", parse_mode=ParseMode.HTML, reply_markup=order_change_builder.as_markup())
    await message.delete()

@router.message(StateFilter(Order.shipper_num), F.contact)
async def order21_1(message: types.Message, state: FSMContext):
    await prev[message.chat.id].delete()
    del prev[message.chat.id]
    order[message.chat.id]['Номер телефона отправителя'] = message.contact.phone_number
    await message.answer('<code>Номер телефона отправителя: ' + message.contact.phone_number+ "</code>", parse_mode=ParseMode.HTML, reply_markup=order_change_builder.as_markup())
    await message.delete()

@router.callback_query(F.data == "change", StateFilter(Order.shipper_num))
async def order_22(callback: types.CallbackQuery, state: FSMContext):
    #  get_phone(message=callback.message)
    prev[callback.message.chat.id] = await callback.message.answer('8️⃣\- *_Введите номер телефона отправителя_*:', reply_markup=order_change_builder.as_markup())
    #  del phone_builder[callback.message.chat.id]
    await callback.message.delete()

@router.callback_query(F.data == "continue", StateFilter(Order.shipper_num))
async def order23(callback: types.CallbackQuery, state: FSMContext):
    prev[callback.message.chat.id] = await callback.message.answer('9️⃣ \- *_Введите ФИО/Название организации получателя_*', reply_markup=get_previous_mrkp(callback.message.chat.id, 'consignee_name'))
    await state.set_state(Order.consignee_name)
    await callback.message.delete()

@router.message(StateFilter(Order.consignee_name))
async def order24(message: types.Message, state: FSMContext):
    await prev[message.chat.id].delete()
    del prev[message.chat.id]
    order[message.chat.id]['ФИО/Название организации получателя'] = message.text
    await message.answer('<code>ФИО/Название организации получателя: ' + message.text+ "</code>", parse_mode=ParseMode.HTML, reply_markup=order_change_builder.as_markup())
    await message.delete()

@router.callback_query(F.data == "change", StateFilter(Order.consignee_name))
async def order_25(callback: types.CallbackQuery, state: FSMContext):
    prev[callback.message.chat.id] = await callback.message.answer('9️⃣ \- *_Введите ФИО/Название организации получателя_*:')
    await callback.message.delete()

@router.callback_query(F.data == "continue", StateFilter(Order.consignee_name))
async def order26(callback: types.CallbackQuery, state: FSMContext):
    prev[callback.message.chat.id] = await callback.message.answer('🔟 \- *_Введите номер телефона получателя_*:', reply_markup=get_previous_mrkp(callback.message.chat.id, 'consignee_phone'))
    await state.set_state(Order.consignee_num)
    await callback.message.delete()

@router.message(StateFilter(Order.consignee_num))
async def order27(message: types.Message, state: FSMContext):
    await prev[message.chat.id].delete()
    del prev[message.chat.id]
    order[message.chat.id]['Номер телефона получателя'] = message.text
    await message.answer('<code>Номер телефона получателя: ' + message.text+ "</code>", parse_mode=ParseMode.HTML, reply_markup=order_change_builder.as_markup())
    await message.delete()

@router.callback_query(F.data == "change", StateFilter(Order.consignee_num))
async def order_28(callback: types.CallbackQuery, state: FSMContext):
    prev[callback.message.chat.id] = await callback.message.answer('🔟\- _*Введите номер телефона получателя*_:', reply_markup=get_previous_mrkp(callback.message.chat.id, 'consignee_phone'))
    await callback.message.delete()
    
@router.callback_query(F.data == "continue", StateFilter(Order.consignee_num))
async def order_check(callback: types.CallbackQuery, state: FSMContext):
    database = get_db()
    try:
        await callback.message.answer('<i>Ваша заявка:</i>\n' + '<code>1 - Аэропорт/город отправления: ' + order[callback.message.chat.id]['Аэропорт/город отправления'] +
                                    '\n2 - Аэропорт/город прибытия: ' + order[callback.message.chat.id]['Аэропорт/город прибытия'] +
                                    '\n3 - Количество мест: ' + order[callback.message.chat.id]['Количество мест'] +
                                    '\n4 - Общий вес груза: ' + order[callback.message.chat.id]['Общий вес груза'] +
                                    '\n5 - Общий объем груза: ' + order[callback.message.chat.id]['Общий объем груза'] +
                                    '\n6 - Планируемая дата привоза на склад: ' + order[callback.message.chat.id]['Планируемая дата привоза на склад'] +
                                    '\n7 - ФИО/Название организации отправителя: ' + order[callback.message.chat.id]['ФИО/Название организации отправителя'] +
                                    '\n8 - Номер телефона отправителя: ' + order[callback.message.chat.id]['Номер телефона отправителя'] +
                                    '\n9 - ФИО/Название организации получателя: ' + order[callback.message.chat.id]['ФИО/Название организации получателя'] +
                                    '\n10 - Номер телефона получателя: ' + order[callback.message.chat.id]['Номер телефона получателя'] + '</code>', 
                                    parse_mode=ParseMode.HTML,
                                        reply_markup=order_send_builder.as_markup()
                                        )
        await database.insert_order(date=datetime.datetime.now(), departure=order[callback.message.chat.id]['Аэропорт/город отправления'],
                                destination=order[callback.message.chat.id]['Аэропорт/город прибытия'], pieces=order[callback.message.chat.id]['Количество мест'],
                                weight=order[callback.message.chat.id]['Общий вес груза'], volume=order[callback.message.chat.id]['Общий объем груза'],
                                warehouse_date=order[callback.message.chat.id]['Планируемая дата привоза на склад'], shipper_name=order[callback.message.chat.id]['ФИО/Название организации отправителя'],
                                shipper_phone=order[callback.message.chat.id]['Номер телефона отправителя'], consignee_name=order[callback.message.chat.id]['ФИО/Название организации получателя'],
                                consignee_phone=order[callback.message.chat.id]['Номер телефона получателя'], user_id=callback.message.chat.id)

        await state.set_state(Order.send)
    except:
        await callback.message.answer("<code>К сожалению, заявка не была отправлена. \nПопробуйте повторить запрос с корректными данными</code>",parse_mode=ParseMode.HTML, reply_markup=menu_builder.as_markup())
        state.set_state(None)
    await callback.message.delete()

@router.callback_query(StateFilter(Order.send), F.data == 'send')
async def order_send(callback: types.callback_query, state: FSMContext):
    await callback.message.edit_text('<code>' + callback.message.text + '</code>', parse_mode=ParseMode.HTML, reply_markup=None)
    mes = '1 - Аэропорт/город отправления: ' + order[callback.message.chat.id]['Аэропорт/город отправления'] +'\n2 - Аэропорт/город прибытия: ' + order[callback.message.chat.id]['Аэропорт/город прибытия'] +'\n3 - Количество мест: ' + order[callback.message.chat.id]['Количество мест'] +'\n4 - Общий вес груза: ' + order[callback.message.chat.id]['Общий вес груза'] +'\n5 - Общий объем груза: ' + order[callback.message.chat.id]['Общий объем груза'] +'\n6 - Планируемая дата привоза на склад: ' + order[callback.message.chat.id]['Планируемая дата привоза на склад'] +'\n7 - ФИО/Название организации отправителя: ' + order[callback.message.chat.id]['ФИО/Название организации отправителя'] +'\n8 - Номер телефона отправителя: ' + order[callback.message.chat.id]['Номер телефона отправителя'] +'\n9 - ФИО/Название организации получвтеля: ' + order[callback.message.chat.id]['ФИО/Название организации получателя'] +'\n10 - Номер телефона получателя: ' + order[callback.message.chat.id]['Номер телефона получателя']
    await callback.message.bot.send_message(chat_id=admin_ids['Gleb'], text = mes, parse_mode=ParseMode.HTML)
    await callback.message.bot.send_message(chat_id=admin_ids['operator'], text = mes, parse_mode=ParseMode.HTML)
    email_send = Send_order()
    await email_send.send_mail(message=mes)
    await callback.message.reply('<i>Заявка успешно отправлена! Наш сотрудник свяжется с Вами в рабочее время</i>', parse_mode = ParseMode.HTML, reply_markup = menu_builder.as_markup())
    del order[callback.message.chat.id]
    await state.set_state(None)

@router.callback_query(F.data == "cancel")
async def order_cancel(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer('Выберите действие', reply_markup=menu_builder.as_markup())
    await state.set_state(None)

# def get_phone(message: types.Message):
#     phone_builder[message.chat.id]= ReplyKeyboardBuilder()
#     phone_builder[message.chat.id].add(types.KeyboardButton(
#         text="Отправить номер телефона",
#         request_contact=True
#     )
#     )

def get_previous_mrkp(user_id, name: str):
    return types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text=i) for i in database.select_order(user_id, name)]], resize_keyboard=True)

def get_time(message: types.Message):
    time_builder[message.chat.id] = ReplyKeyboardBuilder()
    time_builder[message.chat.id].add(types.KeyboardButton(
    text = datetime.date.today().strftime('%d-%m-%y') 
    )
    )

    time_builder[message.chat.id].add(types.KeyboardButton(
    text = (datetime.date.today() + datetime.timedelta(days=1)).strftime('%d-%m-%y') 
    )
    )

    time_builder[message.chat.id].add(types.KeyboardButton(
    text = (datetime.date.today() + datetime.timedelta(days=5)).strftime('%d-%m-%y') 
    )
    )
    time_builder[message.chat.id].adjust(1)