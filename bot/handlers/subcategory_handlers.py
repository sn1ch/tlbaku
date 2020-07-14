import os
from aiogram import types
from aiogram.utils.callback_data import CallbackData
from bot.main import bot, dp
from aiogram.dispatcher.filters import Text
from bot.keyboards.category_mk import navigations, get_subcategory_markup, get_category_markup
from bot.db.models import Botbakuadmin_subcategory, Botbakuadmin_eat, Botbakuadmin_product, Botbakuadmin_beer, \
    Botbakuadmin_category, Botbakuadmin_text
from MyBot.settings import BASE_DIR
from bot.keyboards.product_mk import kb_add


async def send_subcategory_subcategory(call: types.CallbackQuery, callback_data: dict):
    await call.message.edit_reply_markup(reply_markup=await get_subcategory_markup(callback_data['slug_name']))
    await call.answer()


async def back_to_category(call: types.CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=await get_category_markup())
    await call.answer()


async def send_products(call: types.CallbackQuery, callback_data: dict):
    products = await Botbakuadmin_product.all().prefetch_related('beer', 'eat', 'subcategory').filter(
        subcategory__slug_name=callback_data['slug_name'], in_stock=True)
    for product in products:
            try:  # eat1
                text = f'<b>{product.name}</b>\n{product.eat.text}'
            except AttributeError:
                text = f'<b>{product.name.upper()}</b> <i>{product.beer.style.lower()}</i> ' \
                       f'ABV {product.beer.abv}% IBU {product.beer.ibu} OG {product.beer.og}°P'
            photo = types.InputFile(os.path.join(BASE_DIR, product.img))
            await bot.send_photo(call.from_user.id, photo=photo,
                                 caption=text, parse_mode='HTML',
                                 reply_markup=await kb_add(price=product.price, id=product.id))
    subcategory = await Botbakuadmin_subcategory.filter(slug_name=callback_data['slug_name']).prefetch_related(
        'category').values_list('category__slug_name', flat=True)
    await bot.send_message(call.from_user.id, text=f'Всего позиций {len(products)}',
                           reply_markup=await get_subcategory_markup(category=subcategory[0]))
    await call.answer()


def register_subcategory_handlers(dp: dp):
    dp.register_callback_query_handler(back_to_category, Text(equals='back_to_category'))
    dp.register_callback_query_handler(send_subcategory_subcategory, navigations.filter(action='category'))
    dp.register_callback_query_handler(send_products, navigations.filter(action='subcategory'))
