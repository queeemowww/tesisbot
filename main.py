import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, StateFilter
from aiogram.client.default import DefaultBotProperties
from aiogram import F
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from db import Db

from kb.menu_kb import menu_builder
import text
import handlers.order_h as order_h
import handlers.track_h as track_h
import handlers.manager_h as manager_h
import handlers.contacts_h as contacts_h

from aiogram.fsm.context import FSMContext

import os

load_dotenv()

class TesisBot():
    tracker = None
    def __init__(self):
        bot_token = os.getenv('BOT_TOKEN')
        logging.basicConfig(level=logging.INFO)
        self.bot = Bot(token=bot_token, default=DefaultBotProperties(
                parse_mode=ParseMode.MARKDOWN_V2)
                )
        self.dp = Dispatcher()
        self.dp.include_routers(order_h.router, track_h.router, manager_h.router, contacts_h.router)
        self.database = Db()

    async def logic(self):
        # Хэндлер на команду /start
        @self.dp.message(Command("start"))
        async def cmd_start(message: types.Message):
            self.database.insert_user(message.chat.id, message.chat.username)
            await message.answer(
                text.starting_text,
                reply_markup=menu_builder.as_markup()
            )

        @self.dp.message(StateFilter(None), F.text.lower() != 'нюся')
        async def cmd_menu(message: types.Message):
            await message.answer(
                "Выберите действие",
                reply_markup=menu_builder.as_markup()
            )
        "Очистить контекст состояний"
        
        @self.dp.message(Command('clear'))
        async def test(message: types.Message, state: FSMContext):
            await state.set_state(None)
        
    # Запуск процесса поллинга новых апдейтов
    async def main(self):
        await self.logic()
        await self.bot.delete_webhook(drop_pending_updates=True)
        await self.dp.start_polling(self.bot)

if __name__ == "__main__":
    bot = TesisBot()
    asyncio.run(bot.main())