import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, StateFilter
from aiogram.client.default import DefaultBotProperties
from aiogram import F
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from database.db import Db
from database.db_provider import set_db_instance
from kb.menu_kb import menu_builder
import text
import handlers.order_h as order_h
import handlers.track_h as track_h
import handlers.manager_h as manager_h
import handlers.contacts_h as contacts_h
import handlers.fesco_h as fesco_h
import handlers.mycargo_h  as mycargo_h

from aiogram.fsm.context import FSMContext
import os

load_dotenv()
prev = {}
class TesisBot():
    tracker = None
    def __init__(self):
        bot_token = os.getenv('BOT_TOKEN')
        logging.basicConfig(level=logging.INFO)
        self.bot = Bot(token=bot_token, default=DefaultBotProperties(
                parse_mode=ParseMode.MARKDOWN_V2)
                )
        self.dp = Dispatcher()
        self.dp.include_routers(order_h.router, track_h.router, manager_h.router, contacts_h.router, fesco_h.router, mycargo_h.router)

    # async def set_commands(app):
    #     await app.bot.set_my_commands([
    #         Command("start", "Начать работу"),
    #         BotCommand("menu", "Открыть меню"),
    #         BotCommand("help", "Помощь"),
    #         BotCommand("stop", "Остановить бота"),
    #         BotCommand("info", "Обо мне")
    #     ])

    async def logic(self):
        # Хэндлер на команду /start

        @self.dp.message(Command("start"))
        async def cmd_start(message: types.Message):
            try:
                prev[message.chat.id].delete()
            except:
                pass
            self.database = Db()
            await self.database.init()
            set_db_instance(self.database)
            await self.database.insert_user(message.chat.id, message.chat.username, message.chat.first_name, message.chat.last_name)
            prev[message.chat.id] = await message.answer(
                text.starting_text,
                reply_markup=menu_builder.as_markup()
            )

        @self.dp.message(StateFilter(None), F.text.lower() != '/orders', F.text.lower() != 'нюся')
        async def cmd_menu(message: types.Message):
            self.database = Db()
            await self.database.init()
            set_db_instance(self.database)
            await self.database.insert_user(message.chat.id, message.chat.username, message.chat.first_name, message.chat.last_name)
            await message.delete()
            prev[message.chat.id] = await message.answer(
                'Выберите действие\. _для сброса переписки введите_ "/clear"',
                reply_markup=menu_builder.as_markup()
            )
            try:
                await prev[message.chat.id].delete()
            except:
                pass

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