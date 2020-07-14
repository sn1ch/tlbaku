from aiogram import types
from aiogram.dispatcher.filters import Text
from bot.main import bot, dp
from bot.db.models import Botbakuadmin_casinouser, Botbakuadmin_casino
from bot.keyboards.main_mk import main_markup


async def send_casino_text(message: types.Message):
    text = await Botbakuadmin_casino.first().values_list('text', flat=True)
    print(text)
    if text:
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(text='Участвовать!', callback_data='vote_casino'))
        await bot.send_message(message.from_user.id, text=text[0], reply_markup=kb)
    else:
        await bot.send_message(message.from_user.id, text='OPS! Конкурс уже закончился!',
                               reply_markup=await main_markup())


async def push_vote_casino(call: types.CallbackQuery):
    user = await Botbakuadmin_casinouser.get_or_none(user_id=call.from_user.id)
    if user is None:
        await Botbakuadmin_casinouser.create(user_id=call.from_user.id, name=call.from_user.first_name)
        await call.answer('Теперь вы участвуете в конкурсе!')
    else:
        await call.answer('Вы уже участвуете')


def register_handlers_casino(dp: dp):
    dp.register_message_handler(send_casino_text, Text(equals=['КОНКУРС!']))
    dp.register_callback_query_handler(push_vote_casino, Text(equals=['vote_casino']))

