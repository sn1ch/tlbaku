import os

from aiogram import types
from aiogram.dispatcher import FSMContext

from MyBot.settings import BASE_DIR
from bot.keyboards.product_mk import kb_add, order_cart
from bot.state.state import Cart
from bot.main import bot, dp
from bot.db.models import Botbakuadmin_product
from aiogram.dispatcher.filters import Text
from bot.keyboards.cart_mk import get_cart_kb


async def total_sum(data):
    summ = 0
    for k, v in data.items():
        product = await Botbakuadmin_product.filter(id=k)
        summ += product[0].price * v
    return summ


async def add_in_cart(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await query.answer('Позиция добавлена.')
    await bot.answer_callback_query(query.id)
    await Cart.cart.set()
    await state.update_data(page=1)
    async with state.proxy() as data:
        data.setdefault('products', {})
        print(callback_data['id'])
        if callback_data['id'] not in data['products'].keys():
            data['products'].setdefault(callback_data['id'], 1)
        else:
            data['products'][callback_data['id']] += 1
        product = await Botbakuadmin_product.filter(id=int(callback_data['id']))
        await query.message.edit_reply_markup(
            reply_markup=await kb_add(product[0].price, product[0].id,
                                      data['products'][callback_data['id']]))
        print(data)
    await state.reset_state(with_data=False)


async def cart_view_from_msg(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            product_id = list(data['products'].keys())[data['page'] - 1]
            values = list(data['products'].values())[data['page'] - 1]
            product = await Botbakuadmin_product.filter(id=product_id)
            cb_page_text = f'{data["page"]}/{len(data["products"])}'
            totals_sum = await total_sum(data['products'])
            photo = types.InputFile(os.path.join(BASE_DIR, product[0].img))
            await bot.send_photo(message.from_user.id, photo=photo,
                                 caption=f"<b>{product[0].name}</b>", parse_mode='HTML',
                                 reply_markup=get_cart_kb(cb_page_text, values, totals_sum))
    except KeyError:
        await message.answer(text='корзина пуста')


async def cart_view_from_call(call: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            product_id = list(data['products'].keys())[data['page'] - 1]
            values = list(data['products'].values())[data['page'] - 1]
            product = await Botbakuadmin_product.filter(id=product_id)
            cb_page_text = f'{data["page"]}/{len(data["products"])}'
            totals_sum = await total_sum(data['products'])
            photo = types.InputFile(os.path.join(BASE_DIR, product[0].img))
            await bot.send_photo(call.from_user.id, photo=photo,
                                 caption=f"<b>{product[0].name}</b>", parse_mode='HTML',
                                 reply_markup=get_cart_kb(cb_page_text, values, totals_sum))
        await call.answer()
    except KeyError:
        await call.answer(text='корзина пуста')


async def get_prev(call: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id)
    try:
        async with state.proxy() as data:
            if data['page'] > 1:
                data['page'] -= 1
                product_id = list(data['products'].keys())[data['page'] - 1]
                values = list(data['products'].values())[data['page'] - 1]
                product = await Botbakuadmin_product.filter(id=product_id)
                totals_sum = await total_sum(data['products'])
                cb_page_text = f'{data["page"]}/{len(data["products"])}'
                await types.ChatActions.upload_photo()
                photo = types.InputFile(os.path.join(BASE_DIR, product[0].img))
                media = types.InputMediaPhoto(media=photo, caption=f'<b>{product[0].name}</b>',
                                              parse_mode='HTML')
                await call.message.edit_media(media=media, reply_markup=get_cart_kb(cb_page_text, values, totals_sum))
            else:
                pass
    except KeyError:
        await call.answer(text='OPS. Похоже корзина пуста')


async def get_next(call: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id)
    try:
        async with state.proxy() as data:
            if data['page'] < len(data['products']):
                data['page'] += 1
                product_id = list(data['products'].keys())[data['page'] - 1]
                values = list(data['products'].values())[data['page'] - 1]
                product = await Botbakuadmin_product.filter(id=product_id)
                totals_sum = await total_sum(data['products'])
                cb_page_text = f'{data["page"]}/{len(data["products"])}'
                await types.ChatActions.upload_photo()
                photo = types.InputFile(os.path.join(BASE_DIR, product[0].img))
                media = types.InputMediaPhoto(media=photo, caption=f'<b>{product[0].name}</b>',
                                              parse_mode='HTML')
                await call.message.edit_media(media=media, reply_markup=get_cart_kb(cb_page_text, values, totals_sum))
            else:
                pass
    except KeyError:
        await call.answer(text='OPS. Похоже корзина пуста')


async def get_up_item(call: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id)
    try:
        async with state.proxy() as data:
            product_id = list(data['products'].keys())[data['page'] - 1]
            if data['products'][product_id] >= 1:
                data['products'][product_id] += 1
                cb_page_text = f'{data["page"]}/{len(data["products"])}'
                totals_sum = await total_sum(data['products'])
                values = data['products'][product_id]
                await call.message.edit_reply_markup(reply_markup=get_cart_kb(cb_page_text, values, totals_sum))
            else:
                pass
    except KeyError:
        await call.answer(text='OPS. Похоже корзина пуста')


async def get_down_item(call: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id)
    try:
        async with state.proxy() as data:
            product_id = list(data['products'].keys())[data['page'] - 1]
            if data['products'][product_id] > 1:
                data['products'][product_id] -= 1
                cb_page_text = f'{data["page"]}/{len(data["products"])}'
                totals_sum = await total_sum(data['products'])
                values = data['products'][product_id]
                await call.message.edit_reply_markup(reply_markup=get_cart_kb(cb_page_text, values, totals_sum))
            else:
                pass
    except KeyError:
        await call.answer(text='OPS. Похоже корзина пуста')


async def delete_item(call: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id)
    try:
        async with state.proxy() as data:
            if len(data['products']) == 1:
                await state.reset_state(with_data=True)
                await bot.delete_message(call.from_user.id, call.message.message_id)
                await bot.send_message(call.from_user.id, 'корзина пуста')
            else:
                product_id = list(data['products'].keys())[data['page'] - 1]
                data['products'].pop(str(product_id))
                data['page'] = 1
                product_id = list(data['products'].keys())[data['page'] - 1]
                values = list(data['products'].values())[data['page'] - 1]
                product = await Botbakuadmin_product.filter(id=product_id)
                totals_sum = await total_sum(data['products'])
                cb_page_text = f'{data["page"]}/{len(data["products"])}'
                await types.ChatActions.upload_photo()
                photo = types.InputFile(os.path.join(BASE_DIR, product[0].img))
                media = types.InputMediaPhoto(media=photo, caption=f'<b>{product[0].name}</b>',
                                              parse_mode='HTML')
                await call.message.edit_media(media=media, reply_markup=get_cart_kb(cb_page_text, values, totals_sum))
    except KeyError:
        await call.answer(text='OPS. Похоже корзина пуста')


def register_cart_handlers(dp: dp):
    dp.register_callback_query_handler(add_in_cart, order_cart.filter(action='product_add'))
    dp.register_message_handler(cart_view_from_msg, Text(equals='КОРЗИНА'))
    dp.register_callback_query_handler(cart_view_from_call, Text(equals='move_to_cart'))
    dp.register_callback_query_handler(get_prev, Text(equals=['prev']), state='*')
    dp.register_callback_query_handler(get_next, Text(equals=['next']), state='*')
    dp.register_callback_query_handler(get_up_item, Text(equals=['up']), state='*')
    dp.register_callback_query_handler(get_down_item, Text(equals=['down']), state='*')
    dp.register_callback_query_handler(delete_item, Text(equals=['delete']), state='*')
