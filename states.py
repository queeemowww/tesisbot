from aiogram.filters.state import State, StatesGroup 
from aiogram.fsm.context import FSMContext

class Track(StatesGroup):
    airport = State()
    blank = State()
    number = State()
