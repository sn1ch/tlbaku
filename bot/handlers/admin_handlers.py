from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.callback_data import CallbackData
from bot.handlers.main_handler import main_menu
from bot.config import SERG, ANNA
from bot.main import bot, dp
from aiogram.dispatcher.filters import Text
from bot.keyboards.category_mk import navigations, get_subcategory_markup, get_category_markup
from bot.db.models import Botbakuadmin_subcategory, Botbakuadmin_eat, Botbakuadmin_product, Botbakuadmin_beer, \
    Botbakuadmin_category, Botbakuadmin_text
from bot.keyboards.product_mk import kb_add
from bot.state.state import ProductPhoto


async def back_to_category_admin(call: types.CallbackQuery):
    await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id,
                                        reply_markup=await get_category_markup(action='admin_category'))
    await call.answer()


async def admin_panel(message: types.Message):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='Изменить фото', callback_data='change_photo'))
    await bot.send_message(message.from_user.id, text='Держи', reply_markup=kb)


async def admin_main_menu(call: types.CallbackQuery):
    await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id,
                                        reply_markup=await get_category_markup(action='admin_category'))
    await call.answer()


async def admin_send_subcategory_subcategory(call: types.CallbackQuery, callback_data: dict):
    await call.message.edit_reply_markup(
        reply_markup=await get_subcategory_markup(callback_data['slug_name'], action='admin_subcategory'))
    await call.answer()


async def admin_send_products(call: types.CallbackQuery, callback_data: dict):
    products = await Botbakuadmin_product.all().prefetch_related('beer', 'eat', 'subcategory').filter(
        subcategory__slug_name=callback_data['slug_name'], in_stock=True)
    for product in products:
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(text='Изменить фото', callback_data=f'product_change_photo-{product.id}'))
        try:  # eat1
            text = f'<b>{product.name}</b>\n{product.eat.text}'
        except AttributeError:
            text = f'<b>{product.name.upper()}</b> <i>{product.beer.style.lower()}</i> ' \
                   f'ABV {product.beer.abv}% IBU {product.beer.ibu} OG {product.beer.og}°P'
        await bot.send_photo(call.from_user.id, photo=product.img,
                             caption=text,
                             reply_markup=kb, parse_mode='HTML')
    subcategory = await Botbakuadmin_subcategory.filter(slug_name=callback_data['slug_name']).prefetch_related(
        'category').values_list('category__slug_name', flat=True)
    await bot.send_message(call.from_user.id, text=f'Всего позиций {len(products)}',
                           reply_markup=await get_subcategory_markup(category=subcategory[0],
                                                                     action='admin_subcategory',
                                                                     btn_back='back_to_category_admin'))
    await call.answer()


async def update_photo(call: types.CallbackQuery, state: FSMContext):
    await ProductPhoto.product_id.set()
    id = call.data.split(sep='-')
    await state.update_data(product_id=id[-1])
    await bot.send_message(call.from_user.id, 'Отправить фото')
    await call.answer()


async def set_photo(message: types.Message, state: FSMContext):
    product_id = await state.get_data(ProductPhoto.product_id)
    await Botbakuadmin_product.filter(id=int(product_id['product_id'])).update(img=message.photo[-1].file_id)
    await state.finish()
    await bot.send_message(message.from_user.id, 'фото успешно обновлено',
                           reply_markup=await get_category_markup(action='admin_category'))


def register_admin_handlers(dp: dp):
    dp.register_callback_query_handler(back_to_category_admin, Text(equals='back_to_category_admin'))
    dp.register_message_handler(admin_panel, lambda call: call.from_user.id in (int(SERG), ANNA), commands=['admin'])
    dp.register_callback_query_handler(admin_main_menu, Text(equals='change_photo'))
    dp.register_callback_query_handler(admin_send_subcategory_subcategory,
                                       navigations.filter(action='admin_category'))
    dp.register_callback_query_handler(admin_send_products,
                                       navigations.filter(action='admin_subcategory'))
    dp.register_callback_query_handler(update_photo, Text(startswith='product_change_photo'))
    # dp.register_message_handler(set_photo, lambda message: message.from_user.id in (int(SERG), ANNA),
    #                             content_types=['photo'])
    dp.register_message_handler(set_photo,
                                content_types=['photo'], state=ProductPhoto)

    pass

    # dp.register_callback_query_handler(send_subcategory_subcategory, navigations.filter(action='category'))
    # dp.register_callback_query_handler(send_products, navigations.filter(action='subcategory'))
