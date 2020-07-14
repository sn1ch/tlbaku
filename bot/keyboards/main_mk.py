from aiogram import types
from bot.db.models import Botbakuadmin_casino

# main_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
# btn_action = types.KeyboardButton('АКЦИИ ROCKETS & BISHOPS')
# btn_menu = types.KeyboardButton('МЕНЮ ROCKETS & BISHOPS')
# btn_cart = types.KeyboardButton('КОРЗИНА')
# main_markup.add(btn_menu, btn_action, btn_cart)


async def main_markup():
    main_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_action = types.KeyboardButton('АКЦИИ ROCKETS & BISHOPS')
    btn_menu = types.KeyboardButton('МЕНЮ ROCKETS & BISHOPS')
    btn_cart = types.KeyboardButton('КОРЗИНА')
    main_markup.add(btn_menu, btn_action, btn_cart)
    casino = await Botbakuadmin_casino.first()
    if casino is not None:
        main_markup.add('КОНКУРС!')
    return main_markup
