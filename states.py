from aiogram.filters.state import State, StatesGroup 
from aiogram.fsm.context import FSMContext

class Order(StatesGroup):
    departure = State()
    to = State()
    pcs = State()
    weight = State()
    vol = State()
    planned_time = State()
    shipper_name = State()
    shipper_num = State()
    consignee_name = State()
    consignee_num = State()
    send = State()

class Track(StatesGroup):
    airport = State()
    blank = State()
    number = State()

class Manager(StatesGroup):
    manager = State()
