from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


inline_btn_add = InlineKeyboardButton('Добавить', callback_data='add')
inline_add = InlineKeyboardMarkup().add(inline_btn_add)