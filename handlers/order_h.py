
from aiogram import types, Router
from aiogram.types import ReplyKeyboardRemove
from aiogram.filters import Command, StateFilter
from aiogram import F
from aiogram.fsm.context import FSMContext
from kb.order_kb import  order_change_builder, order_phone_builder, order_time_builder, order_send_builder
from kb.order_kb import departure_buttons, destination_buttons, pieces_buttons, weight_buttons, volume_buttons
from kb.order_kb import shipper_name_buttons, shipper_phone_buttons, consignee_name_buttons, consignee_phone_buttons, get_change_awb
from kb.menu_kb import menu_builder
from states import Order
from aiogram.enums import ParseMode
from admin import admin_ids
from database.db_provider import get_db, set_db_instance
from database.db import Db
router = Router()
import datetime
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from utils.email_send import Send_order

admin_id = admin_ids['Gleb']

order = {}
time_builder = {}
phone_builder = {}
prev = {}
change_val = {}

@router.callback_query(F.data == "order", StateFilter(None))
async def order_1(callback: types.CallbackQuery, state: FSMContext):
    database = Db()
    await database.init()
    set_db_instance(database)
    await callback.message.delete()
    order[callback.message.chat.id] = {}
    prev[callback.message.chat.id] = await callback.message.answer('1️⃣ \- *_Введите аэропорт/город отправления_*', reply_markup=await get_previous_mrkp(callback.message.chat.id, 'departure'))
    await state.set_state(Order.departure)

@router.message(StateFilter(Order.departure))
async def order_2(message: types.Message, state: FSMContext):
    await prev[message.chat.id].delete()
    del prev[message.chat.id]
    await message.answer('<code>Аэропорт/город отправления:<b> ' + message.text+ "</b></code>", reply_markup=order_change_builder.as_markup(), parse_mode=ParseMode.HTML)
    order[message.chat.id]['departure'] = message.text
    await message.delete()

@router.callback_query(F.data == "change", StateFilter(Order.departure))
async def order_3(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    prev[callback.message.chat.id] = await callback.message.answer('1️⃣ \- *_Введите аэропорт/город отправления_*',reply_markup=await get_previous_mrkp(callback.message.chat.id, 'departure'))

@router.callback_query(F.data == "continue", StateFilter(Order.departure))
async def order4(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    prev[callback.message.chat.id] = await callback.message.answer('2️⃣ \- *_Введите аэропорт/город прибытия_*',reply_markup=await get_previous_mrkp(callback.message.chat.id, 'destination'))
    await state.set_state(Order.to)

@router.message(StateFilter(Order.to))
async def order_5(message: types.Message, state: FSMContext):
    await prev[message.chat.id].delete()
    del prev[message.chat.id]
    await message.answer('<code>Аэропорт/город прибытия:<b> ' + message.text+ "</b></code>", reply_markup=order_change_builder.as_markup(), parse_mode=ParseMode.HTML)
    order[message.chat.id]['destination'] = message.text
    await message.delete()

@router.callback_query(F.data == "change", StateFilter(Order.to))
async def order_6(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    prev[callback.message.chat.id] = await callback.message.answer('2️⃣ \- *_Введите аэропорт/город прибытия_*', reply_markup=await get_previous_mrkp(callback.message.chat.id, 'destination'))

@router.callback_query(F.data == "continue", StateFilter(Order.to))
async def order7(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    prev[callback.message.chat.id] = await callback.message.answer('3️⃣ \- *_Введите количество мест_*:', reply_markup=await get_previous_mrkp(callback.message.chat.id, 'pieces'))
    await state.set_state(Order.pcs)

@router.message(StateFilter(Order.pcs))
async def order8(message: types.Message, state: FSMContext):
    await prev[message.chat.id].delete()
    del prev[message.chat.id]
    order[message.chat.id]['pieces'] = message.text
    await message.answer('<code>Количество мест:<b> ' + message.text+ "</b></code>", reply_markup=order_change_builder.as_markup(), parse_mode=ParseMode.HTML)
    await message.delete()

@router.callback_query(F.data == "change", StateFilter(Order.pcs))
async def order_9(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    prev[callback.message.chat.id] = await callback.message.answer('4️⃣ \- *_Введите количество мест_*:', reply_markup=await get_previous_mrkp(callback.message.chat.id, 'pieces'))

@router.callback_query(F.data == "continue", StateFilter(Order.pcs),)
async def order10(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    prev[callback.message.chat.id] = await callback.message.answer('4️⃣ - <b><i>Введите общий вес груза(кг)</i></b>:', reply_markup=await get_previous_mrkp(callback.message.chat.id, 'weight'), parse_mode=ParseMode.HTML)
    await state.set_state(Order.weight)

@router.message(StateFilter(Order.weight))
async def order11(message: types.Message, state: FSMContext):
    await prev[message.chat.id].delete()
    del prev[message.chat.id]
    await message.answer('<code>Общий вес груза(кг): ' + message.text+ "</code>", reply_markup=order_change_builder.as_markup(), parse_mode=ParseMode.HTML)
    order[message.chat.id]['weight'] = message.text
    await message.delete()

@router.callback_query(F.data == "change", StateFilter(Order.weight))
async def order_12(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    prev[callback.message.chat.id] = await callback.message.answer('4️⃣ - <b><i>Введите общий вес груза(кг)</i></b>:', reply_markup=await get_previous_mrkp(callback.message.chat.id, 'weight'), parse_mode=ParseMode.HTML)

@router.callback_query(F.data == "continue", StateFilter(Order.weight))
async def order13(callback: types.CallbackQuery, state: FSMContext):
    prev[callback.message.chat.id] = await callback.message.answer('5️⃣ - <b><i>Введите общий объем груза(куб. м)</i></b>:', reply_markup=await get_previous_mrkp(callback.message.chat.id, 'volume'),parse_mode=ParseMode.HTML)
    await state.set_state(Order.vol)
    await callback.message.delete()

@router.message(StateFilter(Order.vol))
async def order12(message: types.Message, state: FSMContext):
    await prev[message.chat.id].delete()
    del prev[message.chat.id]
    await message.answer('<code>Общий объем груза(куб. м): ' + message.text+ "</code>", reply_markup=order_change_builder.as_markup(), parse_mode=ParseMode.HTML)
    order[message.chat.id]['volume'] = message.text
    await message.delete()

@router.callback_query(F.data == "change", StateFilter(Order.vol))
async def order_13(callback: types.CallbackQuery, state: FSMContext):
    prev[callback.message.chat.id] = await callback.message.answer('5️⃣- <b><i>Введите общий объем груза(куб. м)</i></b>:', reply_markup=await get_previous_mrkp(callback.message.chat.id, 'volume'), parse_mode=ParseMode.HTML)
    await callback.message.delete()

@router.callback_query(F.data == "continue", StateFilter(Order.vol))
async def order14(callback: types.CallbackQuery, state: FSMContext):
    await get_time(message=callback.message)
    prev[callback.message.chat.id] = await callback.message.answer('6️⃣\- *_Введите дату привоза груза на склад_*:', reply_markup=time_builder[callback.message.chat.id].as_markup(resize_keyboard = True))
    del time_builder[callback.message.chat.id]
    await state.set_state(Order.planned_time)
    await callback.message.delete()

@router.message(StateFilter(Order.planned_time))
async def order15(message: types.Message, state: FSMContext):
    await prev[message.chat.id].delete()
    del prev[message.chat.id]
    await message.answer('<code>Дата привоза груза на склад: ' + message.text+ "</code>", reply_markup=order_change_builder.as_markup(), parse_mode=ParseMode.HTML)
    order[message.chat.id]['date'] = message.text
    await message.delete()

@router.callback_query(F.data == "change", StateFilter(Order.planned_time))
async def order_16(callback: types.CallbackQuery, state: FSMContext):
    await get_time(message=callback.message)
    prev[callback.message.chat.id] = await callback.message.answer('6️⃣ \- *_Введите дату привоза груза на склад_*:', reply_markup=time_builder[callback.message.chat.id].as_markup(resize_keyboard = True))
    del time_builder[callback.message.chat.id]
    await callback.message.delete()

@router.callback_query(F.data == "continue", StateFilter(Order.planned_time))
async def order17(callback: types.CallbackQuery, state: FSMContext):
    prev[callback.message.chat.id] = await callback.message.answer('7️⃣ \- *_Введите ФИО/Название организации отправителя_*', reply_markup=await get_previous_mrkp(callback.message.chat.id, 'shipper_name'))
    await state.set_state(Order.shipper_name)
    await callback.message.delete()

@router.message(StateFilter(Order.shipper_name))
async def order18(message: types.Message, state: FSMContext):
    await prev[message.chat.id].delete()
    del prev[message.chat.id]
    order[message.chat.id]['shfio'] = message.text
    await message.answer('<code>ФИО/Название организации отправителя: ' + message.text+ "</code>", parse_mode=ParseMode.HTML, reply_markup=order_change_builder.as_markup())
    await message.delete()

@router.callback_query(F.data == "change", StateFilter(Order.shipper_name))
async def order_19(callback: types.CallbackQuery, state: FSMContext):
    prev[callback.message.chat.id] = await callback.message.answer('7️⃣ \- *_Введите ФИО/Название организации отправителя_*:', reply_markup=await get_previous_mrkp(callback.message.chat.id, 'shipper_name'))
    await callback.message.delete()

@router.callback_query(F.data == "continue", StateFilter(Order.shipper_name))
async def order20(callback: types.CallbackQuery, state: FSMContext):
    # get_phone(message=callback.message)
    prev[callback.message.chat.id] = await callback.message.answer('8️⃣\- *_Введите номер телефона отправителя_*', reply_markup=await get_previous_mrkp(callback.message.chat.id, 'shipper_phone'))
    # del phone_builder[callback.message.chat.id]
    await state.set_state(Order.shipper_num)
    await callback.message.delete()

@router.message(StateFilter(Order.shipper_num), F.text)
async def order21(message: types.Message, state: FSMContext):
    await prev[message.chat.id].delete()
    del prev[message.chat.id]
    order[message.chat.id]['shphone'] = message.text
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
    prev[callback.message.chat.id] = await callback.message.answer('9️⃣ \- *_Введите ФИО/Название организации получателя_*', reply_markup=await get_previous_mrkp(callback.message.chat.id, 'consignee_name'))
    await state.set_state(Order.consignee_name)
    await callback.message.delete()

@router.message(StateFilter(Order.consignee_name))
async def order24(message: types.Message, state: FSMContext):
    await prev[message.chat.id].delete()
    del prev[message.chat.id]
    order[message.chat.id]['cnfio'] = message.text
    await message.answer('<code>ФИО/Название организации получателя: ' + message.text+ "</code>", parse_mode=ParseMode.HTML, reply_markup=order_change_builder.as_markup())
    await message.delete()

@router.callback_query(F.data == "change", StateFilter(Order.consignee_name))
async def order_25(callback: types.CallbackQuery, state: FSMContext):
    prev[callback.message.chat.id] = await callback.message.answer('9️⃣ \- *_Введите ФИО/Название организации получателя_*:')
    await callback.message.delete()

@router.callback_query(F.data == "continue", StateFilter(Order.consignee_name))
async def order26(callback: types.CallbackQuery, state: FSMContext):
    prev[callback.message.chat.id] = await callback.message.answer('🔟 \- *_Введите номер телефона получателя_*:', reply_markup=await get_previous_mrkp(callback.message.chat.id, 'consignee_phone'))
    await state.set_state(Order.consignee_num)
    await callback.message.delete()

@router.message(StateFilter(Order.consignee_num))
async def order27(message: types.Message, state: FSMContext):
    await prev[message.chat.id].delete()
    del prev[message.chat.id]
    order[message.chat.id]['cnphone'] = message.text
    await message.answer('<code>Номер телефона получателя: ' + message.text+ "</code>", parse_mode=ParseMode.HTML, reply_markup=order_change_builder.as_markup())
    await message.delete()

@router.callback_query(F.data == "change", StateFilter(Order.consignee_num))
async def order_28(callback: types.CallbackQuery, state: FSMContext):
    prev[callback.message.chat.id] = await callback.message.answer('🔟\- _*Введите номер телефона получателя*_:', reply_markup=await get_previous_mrkp(callback.message.chat.id, 'consignee_phone'))
    await callback.message.delete()
    
@router.callback_query(F.data == "continue", StateFilter(Order.consignee_num))
async def order_check(callback: types.CallbackQuery, state: FSMContext):
    database = get_db()
    # try:
    prev[callback.message.chat.id] = await callback.message.answer('Ваша заявка <i>(Выберите параметр для изменения или нажмите продолжить ✅)</i>', reply_markup=await get_change_awb(pcs=order[callback.message.chat.id]['pieces'],
                                                                            w = order[callback.message.chat.id]['weight'],
                                                                            v = order[callback.message.chat.id]['volume'],
                                                                            fr = order[callback.message.chat.id]['departure'],
                                                                            dest = order[callback.message.chat.id]['destination'],
                                                                            date = order[callback.message.chat.id]['date'],
                                                                            shipper_fio=order[callback.message.chat.id]['shfio'],
                                                                            shipper_phone=order[callback.message.chat.id]['shphone'],
                                                                            consignee_fio=order[callback.message.chat.id]['cnfio'],
                                                                            consignee_phone=order[callback.message.chat.id]['cnphone']
                                                                            ), parse_mode=ParseMode.HTML)

    await database.insert_order(date=datetime.datetime.now(), departure=order[callback.message.chat.id]['departure'],
                            destination=order[callback.message.chat.id]['destination'], pieces=order[callback.message.chat.id]['pieces'],
                            weight=order[callback.message.chat.id]['weight'], volume=order[callback.message.chat.id]['volume'],
                            warehouse_date=order[callback.message.chat.id]['date'], shipper_name=order[callback.message.chat.id]['shfio'],
                            shipper_phone=order[callback.message.chat.id]['shphone'], consignee_name=order[callback.message.chat.id]['cnfio'],
                            consignee_phone=order[callback.message.chat.id]['cnphone'], user_id=callback.message.chat.id)

    await state.set_state(Order.send)
    # except:
    #     await callback.message.answer("<code>К сожалению, заявка не была отправлена. \nПопробуйте повторить запрос с корректными данными</code>",parse_mode=ParseMode.HTML, reply_markup=menu_builder.as_markup())
    #     await state.set_state(None)
    # await callback.message.delete()

@router.callback_query(StateFilter(Order.send), F.data != 'go', F.data != 'cancel', F.data != 'close', F.data != 'change', F.data != 'continue')
async def order_change1(callback: types.CallbackQuery, state: FSMContext):
    print('pick')
    await prev[callback.message.chat.id].delete()
    parameters = {
        'pieces': "количество мест",
        'weight': 'общий вес груза',
        'volume': 'общий объем груза',
        'departure': 'аэропорт/город отправления',
        'destination': 'аэропорт/город прибытия',
        'date': 'дата привоза груза',
        'shfio': 'ФИО/наименование отправителя',
        'shphone': 'контактный номер телефона отправителя',
        'cnfio': 'ФИО/наименование получателя',
        'cnphone': 'контактный номер телефона получателя'
    }
    
    parameters_roditelniy = {
        'pieces': "количества мест",
        'weight': 'общего веса груза',
        'volume': 'общего объема груза',
        'departure': 'аэропорта/города отправления',
        'destination': 'аэропорта/города прибытия',
        'date': 'даты привоза груза',
        'shfio': 'ФИО/наименования отправителя',
        'shphone': 'контактного номера телефона отправителя',
        'cnfio': 'ФИО/наименования получателя',
        'cnphone': 'контактного номера телефона получателя'
    }
    prev[callback.message.chat.id] = await callback.message.answer(f'Введите новое значение для <b>{parameters_roditelniy[callback.data]}</b>', parse_mode=ParseMode.HTML)
    change_val[callback.message.chat.id] = callback.data

@router.message(StateFilter(Order.send))
async def order_change2(message: types.Message, state: FSMContext):
    print('confirm')
    await prev[message.chat.id].delete()
    await message.delete()
    print(order[message.chat.id], message.text)
    prev[message.chat.id] = await message.answer(f'<b>{change_val[message.chat.id]}: {message.text}</b>', reply_markup=order_change_builder.as_markup(), parse_mode= ParseMode.HTML)
    order[message.chat.id][change_val[message.chat.id]] = message.text
    print(order[message.chat.id], message.text)
    await state.set_state(Order.new)

@router.callback_query(StateFilter(Order.new), F.data == 'continue')
async def order_new1(callback: types.callback_query, state: FSMContext):
    database = get_db()
    await prev[callback.message.chat.id].delete()
    prev[callback.message.chat.id] = await callback.message.answer('Ваша заявка <i>(Выберите параметр для изменения или нажмите продолжить ✅)</i>', reply_markup=await get_change_awb(pcs=order[callback.message.chat.id]['pieces'],
                                                                            w = order[callback.message.chat.id]['weight'],
                                                                            v = order[callback.message.chat.id]['volume'],
                                                                            fr = order[callback.message.chat.id]['departure'],
                                                                            dest = order[callback.message.chat.id]['destination'],
                                                                            date = order[callback.message.chat.id]['date'],
                                                                            shipper_fio=order[callback.message.chat.id]['shfio'],
                                                                            shipper_phone=order[callback.message.chat.id]['shphone'],
                                                                            consignee_fio=order[callback.message.chat.id]['cnfio'],
                                                                            consignee_phone=order[callback.message.chat.id]['cnphone']
                                                                            ), parse_mode=ParseMode.HTML)

    await database.insert_order(date=datetime.datetime.now(), departure=order[callback.message.chat.id]['departure'],
                            destination=order[callback.message.chat.id]['destination'], pieces=order[callback.message.chat.id]['pieces'],
                            weight=order[callback.message.chat.id]['weight'], volume=order[callback.message.chat.id]['volume'],
                            warehouse_date=order[callback.message.chat.id]['date'], shipper_name=order[callback.message.chat.id]['shfio'],
                            shipper_phone=order[callback.message.chat.id]['shphone'], consignee_name=order[callback.message.chat.id]['cnfio'],
                            consignee_phone=order[callback.message.chat.id]['cnphone'], user_id=callback.message.chat.id)
    await state.set_state(Order.send)

@router.callback_query(StateFilter(Order.new), F.data == 'change')
async def order_new2(callback: types.callback_query, state: FSMContext):
    parameters_roditelniy = {
        'pieces': "количества мест",
        'weight': 'общего веса груза',
        'volume': 'общего объема груза',
        'departure': 'аэропорта/города отправления',
        'destination': 'аэропорта/города прибытия',
        'date': 'даты привоза груза',
        'shfio': 'ФИО/наименования отправителя',
        'shphone': 'ФИО/наименования получателя',
        'cnfio': 'контактного номера телефона отправителя',
        'cnphone': 'контактного номера телефона получателя'
    }
    await prev[callback.message.chat.id].delete()
    prev[callback.message.chat.id] = await callback.message.answer(f'Введите новое значение для <b>{parameters_roditelniy[callback.data]}</b>', parse_mode=ParseMode.HTML)
    change_val[callback.message.chat.id] = callback.data

# @router.callback_query(StateFilter(Order.send), F.data == 'change')
# async def order_change3(callback: types.callback_query, state: FSMContext):
#     parameters_roditelniy = {
#         'pieces': "количества мест",
#         'weight': 'общего веса груза',
#         'volume': 'общего объема груза',
#         'departure': 'аэропорта/города отправления',
#         'destination': 'аэропорта/города прибытия',
#         'date': 'даты привоза груза',
#         'shfio': 'ФИО/наименования отправителя',
#         'shphone': 'ФИО/наименования получателя',
#         'cnfio': 'контактного номера телефона отправителя',
#         'cnphone': 'контактного номера телефона получателя'
#     }
#     await prev[callback.message.chat.id].delete()
#     prev[callback.message.chat.id] = await callback.message.answer(f'Введите новое значение для <b>{parameters_roditelniy[callback.data]}</b>', parse_mode=ParseMode.HTML)
#     change_val[callback.message.chat.id] = callback.data


@router.callback_query(StateFilter(Order.send), F.data == 'go')
async def order_send(callback: types.callback_query, state: FSMContext):
    mes = '1 - Аэропорт/город отправления: ' + order[callback.message.chat.id]['departure'] +'\n2 - Аэропорт/город прибытия: ' + order[callback.message.chat.id]['destination'] +'\n3 - Количество мест: ' + order[callback.message.chat.id]['pieces'] +'\n4 - Общий вес груза: ' + order[callback.message.chat.id]['weight'] +'\n5 - Общий объем груза: ' + order[callback.message.chat.id]['volume'] +'\n6 - Планируемая дата привоза на склад: ' + order[callback.message.chat.id]['date'] +'\n7 - ФИО/Название организации отправителя: ' + order[callback.message.chat.id]['shfio'] +'\n8 - Номер телефона отправителя: ' + order[callback.message.chat.id]['shphone'] +'\n9 - ФИО/Название организации получвтеля: ' + order[callback.message.chat.id]['cnfio'] +'\n10 - Номер телефона получателя: ' + order[callback.message.chat.id]['cnphone']
    await prev[callback.message.chat.id].edit_text("<i>Ваша заявка:</i><code>"+mes+"</code>", parse_mode = ParseMode.HTML, reply_markup = None)
    await callback.message.bot.send_message(chat_id=admin_ids['Gleb'], text = mes, parse_mode=ParseMode.HTML)
    await callback.message.bot.send_message(chat_id=admin_ids['operator'], text = mes, parse_mode=ParseMode.HTML)
    email_send = Send_order()
    await email_send.send_mail(message=mes)
    await callback.message.reply('<i>Заявка успешно отправлена! Наш сотрудник свяжется с Вами в рабочее время</i>', parse_mode = ParseMode.HTML, reply_markup = menu_builder.as_markup())
    del order[callback.message.chat.id]
    del prev[callback.message.chat.id]
    await state.set_state(None)

@router.callback_query(F.data == "cancel")
async def order_cancel(callback: types.CallbackQuery, state: FSMContext):
    try:
        del order[callback.message.chat.id]
        del time_builder[callback.message.chat.id]
    except:
        pass
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

async def get_previous_mrkp(user_id, name: str):
    database = get_db()
    get_prv_bldr = ReplyKeyboardBuilder()
    btns = [types.KeyboardButton(text=i) for i in await database.select_order(user_id, name)]
    for btn in btns:
        get_prv_bldr.row(btn)
    return get_prv_bldr.as_markup(resize_keyboard = True)

    # return types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text=i) for i in await database.select_order(user_id, name)]])

async def get_time(message: types.Message):
    time_builder[message.chat.id] = ReplyKeyboardBuilder()
    time_builder[message.chat.id].row(types.KeyboardButton(
    text = datetime.date.today().strftime('%d-%m-%y') 
    )
    )

    time_builder[message.chat.id].row(types.KeyboardButton(
    text = (datetime.date.today() + datetime.timedelta(days=1)).strftime('%d-%m-%y') 
    )
    )

    time_builder[message.chat.id].row(types.KeyboardButton(
    text = (datetime.date.today() + datetime.timedelta(days=5)).strftime('%d-%m-%y') 
    )
    )
    time_builder[message.chat.id].adjust(1)