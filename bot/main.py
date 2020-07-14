import asyncio
import logging
from aiogram import Bot, Dispatcher, executor
from tortoise import Tortoise
from bot.db.models import Botbakuadmin_subcategory, Botbakuadmin_product, Botbakuadmin_eat, Botbakuadmin_beer, \
    Botbakuadmin_category, Botbakuadmin_text, Botbakuadmin_tguser, Botbakuadmin_casino, Botbakuadmin_casinouser
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot.config import TOKEN

logging.basicConfig(level=logging.INFO)
loop = asyncio.get_event_loop()
loop.run_until_complete(
    Tortoise.init(db_url="postgres://admin:admin@localhost/test2", modules={"models": ["__main__"]}))
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage, loop=loop)

if __name__ == '__main__':
    from bot.handlers.register_handlers import *
    executor.start_polling(dp, skip_updates=True)
