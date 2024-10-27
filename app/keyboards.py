from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


client_reply_keyboards = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Купить монеты')],
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
    [InlineKeyboardButton(text='Отменить', callback_data='cancel')]
])


check_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Проверить', callback_data='check')]
])

cancel_two_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отмена', callback_data='cancel_two')]
])

quantity_buy_point_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='1', callback_data='one_point'), InlineKeyboardButton(text='2', callback_data='two_point'), InlineKeyboardButton(text='3', callback_data='tree_point')],
    [InlineKeyboardButton(text='5', callback_data='five_point'), InlineKeyboardButton(text='10', callback_data='ten_point')],
])