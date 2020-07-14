from aiogram import types
from aiogram.utils.callback_data import CallbackData

order_cart = CallbackData('nav', 'action', 'id')


async def kb_add(price: str, id: str, quantity=0) -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=1)
    if quantity:
        kb.add(types.InlineKeyboardButton(text=f'Добавить в корзину - {price}₽ ({quantity})',
                                          callback_data=order_cart.new(action='product_add', id=id)))
        kb.row(types.InlineKeyboardButton(text='Перейти в корзину', callback_data='move_to_cart'))
    else:
        kb.add(types.InlineKeyboardButton(text=f'Добавить в корзину - {price}₽',
                                          callback_data=order_cart.new(action='product_add', id=id)))

    return kb
