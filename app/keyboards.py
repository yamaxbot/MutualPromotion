from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


client_reply_keyboards = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='📈Заработать монеты'), KeyboardButton(text='🛒Купить услуги')],
    [KeyboardButton(text='🏦Баланс')]

], resize_keyboard=True, input_field_placeholder='Введите...')


buy_otzuv_moderation_ = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Одобрить', callback_data='approve'), InlineKeyboardButton(text='Отклонить', callback_data='reject')]
])

pass_otzuv_moderation_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Одобрить', callback_data='approve_pass'), InlineKeyboardButton(text='Отклонить', callback_data='reject_pass')]
])

cancel_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отменить', callback_data='cancel')]
])


check_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Проверить', callback_data='check')]
])

cancel_two_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отмена', callback_data='cancel_two')]
])