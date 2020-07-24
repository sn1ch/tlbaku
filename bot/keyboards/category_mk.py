from aiogram.utils.callback_data import CallbackData
from bot.db.models import Botbakuadmin_category, Botbakuadmin_subcategory
from aiogram import types

navigations = CallbackData('nav', 'action', 'slug_name')


async def get_category_markup(action='category') -> types.InlineKeyboardMarkup:
    categorys = await Botbakuadmin_category.all().values_list('name', 'slug_name')
    mk = types.InlineKeyboardMarkup()
    mk.add(
        *[types.InlineKeyboardButton(text=category_name.upper(),
                                     callback_data=navigations.new(action=action, slug_name=category_slug)) for
          category_name, category_slug in categorys])

    return mk


async def get_subcategory_markup(category: str, action='subcategory',
                                 btn_back='back_to_category') -> types.InlineKeyboardMarkup:
    emoji_back = u'\U000021AA'
    subcategorys = await Botbakuadmin_subcategory.all().prefetch_related('category').filter(
        category__slug_name=category).values_list('name', 'slug_name')
    mk = types.InlineKeyboardMarkup(row_width=2)
    mk.add(
        *[types.InlineKeyboardButton(text=subcategory_name.upper(),
                                     callback_data=navigations.new(action=action, slug_name=subcategory_slug))
          for subcategory_name, subcategory_slug in subcategorys])
    mk.row(types.InlineKeyboardButton(text=f'{emoji_back}НАЗАД', callback_data=btn_back))
    return mk
