from aiogram import types

order_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
btn_yes = types.KeyboardButton('ВЕРНО')
btn_back = types.KeyboardButton('НАЗАД')
order_menu.add(btn_yes, btn_back)

back_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
back_menu.add(btn_back)

order_phone_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
btn_get_phone = types.KeyboardButton('ОТПРАВИТЬ ТЕЛЕФОН', request_contact=True)
order_phone_menu.add(btn_get_phone, btn_back)

order_check_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
btn_accept_order = types.KeyboardButton('ЗАКАЗ ВЕРЕН')
order_check_menu.add(btn_accept_order, btn_back)
