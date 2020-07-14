from aiogram import types
from bot.db.models import *

emoji = {
    'green_check_box': u'\U00002705',
    'cross_mark': u'\U0000274C',
    'prev': u'\U00002B05',
    'next': u'\U000027A1',
    'up': u'\U00002795',
    'down': u'\U00002796'
}


def get_cart_kb(text, items, total_sum=0):
    kb = types.InlineKeyboardMarkup(row_width=3)
    left = types.InlineKeyboardButton(text=emoji['prev'], callback_data='prev')
    right = types.InlineKeyboardButton(text=emoji['next'], callback_data='next')
    centr = types.InlineKeyboardButton(text=text, callback_data='3')
    up = types.InlineKeyboardButton(text=emoji['up'], callback_data='up')
    down = types.InlineKeyboardButton(text=emoji['down'], callback_data='down')
    q = types.InlineKeyboardButton(text=f'{items} шт.', callback_data='3')
    del_items = types.InlineKeyboardButton(text=emoji['cross_mark'], callback_data='delete')
    order = types.InlineKeyboardButton(text=f'{emoji["green_check_box"]} {total_sum} руб. Оформить заказ?',
                                       callback_data='to_order')
    kb.row(del_items, down, q, up)
    kb.add(left, centr, right)
    kb.add(order)
    return kb