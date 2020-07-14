from bot.db.models import Botbakuadmin_subcategory, Botbakuadmin_eat, Botbakuadmin_product, Botbakuadmin_beer, \
    Botbakuadmin_category, Botbakuadmin_text, Botbakuadmin_tguser, Botbakuadmin_casino
from aiogram import types
from aiogram.utils.callback_data import CallbackData
from bot.main import bot, dp
from aiogram.dispatcher.filters import Text
from bot.keyboards.main_mk import main_markup
from bot.keyboards.category_mk import get_category_markup


async def send_welcome(message: types.Message):
    print(message)
    text = await Botbakuadmin_text.filter(slug_name='privetsvie').values_list('text', flat=True)
    # await message.reply(*text, reply_markup=main_markup, parse_mode='HTML')
    await message.reply(*text, reply_markup=await main_markup())
    print(await Botbakuadmin_casino.first())


async def main_menu(message: types.Message):
    await message.reply('Выбери раздел ROCKETS & BISHOPS', reply_markup=await get_category_markup())


async def send_actions(message: types.Message):
    text = await Botbakuadmin_text.filter(slug_name='akcii').values_list('text', flat=True)
    await message.reply(*text)


def register_start_handlers(dp: dp):
    dp.register_message_handler(send_welcome, commands=['start', 'help'])
    dp.register_message_handler(main_menu, Text(equals=['МЕНЮ ROCKETS & BISHOPS']))
    dp.register_message_handler(send_actions, Text(equals=['АКЦИИ ROCKETS & BISHOPS']))
