from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from bot.config import ORDER_CHAT_ROKETS, ORDER_CHAT_ADMIN
from bot.keyboards.order_mk import back_menu, order_menu, order_phone_menu, order_check_menu
from bot.main import bot, dp
from bot.keyboards.main_mk import main_markup
from bot.state.state import Cart
from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher.filters import Text
from bot.db.models import Botbakuadmin_product, Botbakuadmin_tguser
import re

order_user_id = CallbackData('order', 'user', 'id', 'name')


async def cancel_order(message: types.Message, state: FSMContext):
    await message.reply('Главное меню', reply_markup=await main_markup())
    await state.reset_state(with_data=False)


async def start_order(call: types.CallbackQuery, state: FSMContext):
    msg = '<b>Внимание!</b> Возможен только самовывоз.\nЗаказ можно забрать по адресу: ' \
          'ул.Гороховая 2, с 13 до 22 часов.\n\nМы свяжемся с вами для подтверждения заказа!'
    await bot.send_message(call.message.chat.id, msg, parse_mode='HTML')
    await Cart.bar.set()
    await state.update_data(bar=ORDER_CHAT_ROKETS)
    await bot.send_message(call.from_user.id, f'Когда придете за заказом?\n', reply_markup=back_menu)
    await Cart.time.set()
    await call.answer()


async def get_time(message: types.Message, state: FSMContext):
    if message.text not in ['НАЗАД', None, 'ВЕРНО']:
        time = message.text
        await state.update_data(time=time)
        await message.answer(f'Как вас зовут?\nСейчас: {message.from_user.first_name}', reply_markup=order_menu)
        await Cart.name.set()
    elif message.text == 'НАЗАД':
        await state.reset_state(with_data=False)
        await message.reply('Главное меню', reply_markup=await main_markup())


async def get_name(message: types.Message, state: FSMContext):
    print(message.text.lower())
    if message.text.lower() not in ['назад', None, 'верно', 'да']:
        name = message.text
        await state.update_data(name=name)
        await message.answer('Введите свой контактный телефон', reply_markup=order_phone_menu)
        await Cart.phone.set()
    elif message.text.lower() in ['верно', 'да']:
        name = message.from_user.first_name
        await state.update_data(name=name)
        await message.answer('Введите свой контактный телефон', reply_markup=order_phone_menu)
        await Cart.phone.set()
    elif message.text.lower() == 'назад':
        await state.reset_state(with_data=False)
        await message.reply('Главное меню', reply_markup=await main_markup())


async def get_phone_invalid(message: types.Message):
    return await message.reply('Телефон должен быть числом.\nВведите свой контактный телефон(только цифры)')


async def get_phone_contact(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number
    await state.update_data(phone=phone)
    await message.answer('Вот ваш заказ, все верно?')
    product_list = []
    async with state.proxy() as data:
        summ = 0
        for product_id, q in data['products'].items():
            product = await Botbakuadmin_product.filter(id=product_id).values('name', 'price', 'subcategory__id',
                                                                              'subcategory__name', 'beer_id')
            if product[0]['beer_id'] is None:
                text_part = \
                    f'<b>{product[0]["name"].upper()}</b> {product[0]["subcategory__name"].capitalize()} -{q} шт.'
            else:
                text_part = f'<b>{product[0]["name"]} </b> {product[0]["subcategory__name"].capitalize()} -{q} л.'
            summ += product[0]['price'] * q
            product_list.append(text_part)
        template = ("Сумма: {}₽\nЗаберу: {}\n{}\n{}".format(summ, data["time"], data["name"], data["phone"]))
        product_list.append(template)
        msg = '\n'.join(product_list)
        await message.answer(text=msg, reply_markup=order_check_menu, parse_mode='HTML')
    await Cart.user_id.set()


async def get_phone_digit(message: types.Message, state: FSMContext):
    if message.text.lower() == 'назад':
        await state.reset_state()
        await message.reply('Главное меню', reply_markup=await main_markup())
    else:
        phone = message.text
        pattern_phone = \
            '((8|\+7)[\- ]?)?(\()?(\d{3})?(\))?[\- ]?(\d{3})?[\- ]?(\d{2})?[\- ]?(\d{2})(\s*)(\()?(доб.)*(\s)?(\d{4})?(\))?'
        new_phone_format = re.sub(pattern_phone, r"+7\4\6\7\8", phone)
        await state.update_data(phone=new_phone_format)
        await message.answer('Вот ваш заказ, все верно?')
        product_list = []
        async with state.proxy() as data:
            summ = 0
            for product_id, q in data['products'].items():
                product = await Botbakuadmin_product.filter(id=product_id).values('name', 'price', 'subcategory__id',
                                                                                  'subcategory__name', 'beer_id')
                if product[0]['beer_id'] is None:
                    text_part = \
                        f'<b>{product[0]["name"].upper()}</b> {product[0]["subcategory__name"].capitalize()} -{q} шт.'
                else:
                    text_part = f'<b>{product[0]["name"]} </b> {product[0]["subcategory__name"].capitalize()} -{q} л.'
                summ += product[0]['price'] * q
                product_list.append(text_part)
            template = ("Сумма: {}₽\nЗаберу: {}\n{}\n{}".format(summ, data["time"], data["name"], data["phone"]))
            product_list.append(template)
            msg = '\n'.join(product_list)
            await message.answer(text=msg, reply_markup=order_check_menu, parse_mode='HTML')
        await Cart.user_id.set()


async def check_order(message: types.Message, state: FSMContext):
    if message.text.lower() == 'назад':
        await state.reset_state()
        await message.reply('Главное меню', reply_markup=await main_markup())
    if message.text.lower() == 'заказ верен':
        await state.update_data(user_id=message.from_user.id)
        product_list = []
        async with state.proxy() as data:
            summ = 0
            for id, q in data['products'].items():
                product = await Botbakuadmin_product.filter(id=id).values('name', 'price', 'subcategory__id',
                                                                          'subcategory__name', 'beer_id')
                if product[0]['beer_id'] is None:
                    text_part = f'<b>{product[0]["name"].upper()}</b> {product[0]["subcategory__name"].capitalize()} -{q} шт.'
                else:
                    text_part = f'<b>{product[0]["name"]} </b> {product[0]["subcategory__name"].capitalize()} -{q} л.'
                summ += product[0]['price'] * q
                product_list.append(text_part)
            template = ("Сумма: {}₽\nЗаберу: {}\n{}\n{}".format(summ, data["time"], data["name"], data["phone"]))
            product_list.append(template)
            msg = '\n'.join(product_list)
            user = await Botbakuadmin_tguser.get_or_none(user_id=message.from_user.id)
            if user is None:
                await Botbakuadmin_tguser.create(user_id=message.from_user.id, name=data["name"], phone=data["phone"])
            else:
                await user.save()
            admin_order_check_menu = types.InlineKeyboardMarkup()
            btn_admin_order_check = types.InlineKeyboardButton(text='ЗАКАЗ СОБРАН',
                                                               callback_data=order_user_id.new(user='user',
                                                                                               id=data['user_id'],
                                                                                               name=data['name']))
            admin_order_check_menu.add(btn_admin_order_check)
            await bot.send_message(data['bar'], msg, reply_markup=admin_order_check_menu, parse_mode='HTML')
            await bot.send_message(ORDER_CHAT_ADMIN, 'РОКЕТС \n' + msg, parse_mode='HTML')  # админ чат
            await message.answer('Ваш заказ принят в обработку, наш сотрудник свяжется с вами в ближайшее время',
                                 reply_markup=await main_markup())
            await state.finish()


async def admin(query: types.CallbackQuery, callback_data: dict):
    user_id = callback_data['id']
    user_name = callback_data['name']
    await bot.send_message(user_id, f'{user_name}, ваш заказ собран и готов к выдаче!')
    await bot.edit_message_reply_markup(ORDER_CHAT_ROKETS, query.message.message_id, reply_markup='')
    await bot.send_message(ORDER_CHAT_ROKETS, 'Сообщение о готовности заказа отправленно пользователю.',
                           reply_to_message_id=query.message.message_id)
    await bot.send_message(ORDER_CHAT_ADMIN, 'Рокетс подтвердили готовность заказа нажатием кнопки')


def register_handlers_order(dp: dp):
    dp.register_message_handler(cancel_order, Text(equals=['НАЗАД']), state='*')
    dp.register_callback_query_handler(start_order, Text(equals=['to_order']))
    dp.register_message_handler(get_time, state=Cart.time)
    dp.register_message_handler(get_name, state=Cart.name)
    dp.register_message_handler(get_phone_invalid,
                                lambda message: not message.text.isdigit() and message.text.lower() not in (
                                    'назад', 'заказ верен'), state=Cart.phone)
    dp.register_message_handler(get_phone_contact, state=Cart.phone, content_types=['contact'])
    dp.register_message_handler(get_phone_digit, state=Cart.phone,
                                content_types=['text'])
    dp.register_message_handler(check_order, lambda message: message.text.lower() in ('назад', 'заказ верен'),
                                state=Cart.user_id)
    dp.register_callback_query_handler(admin, order_user_id.filter(user='user'))
