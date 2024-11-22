from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


client_reply_keyboards = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='💫Купить монеты'), KeyboardButton(text='🎁Промокоды')],
    [KeyboardButton(text='📈Заработать монеты'), KeyboardButton(text='🛒Купить услуги')],
    [KeyboardButton(text='🫂Реферальная система'), KeyboardButton(text='🏦Баланс')]

], resize_keyboard=True, input_field_placeholder='Введите...')


buy_otzuv_moderation_ = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Одобрить', callback_data='approve'), InlineKeyboardButton(text='Отклонить', callback_data='reject')]
])

pass_otzuv_moderation_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Одобрить', callback_data='approve_pass'), InlineKeyboardButton(text='Отклонить', callback_data='reject_pass')]
])

cancel_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отменить', callback_data='cancel'), InlineKeyboardButton(text='Пожаловаться', callback_data='сomplain')]
])


check_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Проверить', callback_data='check')]
])

cancel_two_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отмена', callback_data='cancel_two')]
])

quantity_buy_point_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🪙2 - ⭐1', callback_data='one_point_ik'), InlineKeyboardButton(text='🪙10 - ⭐5', callback_data='five_point_ik')],
    [InlineKeyboardButton(text='🪙20 - ⭐10', callback_data='ten_point_ik')],
    [InlineKeyboardButton(text='🪙50 - ⭐25', callback_data='twentyfive_point_ik')]
])


promo_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='🛒Создать промокод')],
    [KeyboardButton(text='✒️Ввести промокод')],
    [KeyboardButton(text='🔙На главную')]

], resize_keyboard=True, input_field_placeholder='Введите...')