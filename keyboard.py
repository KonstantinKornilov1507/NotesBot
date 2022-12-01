from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

button_make = InlineKeyboardButton('Сделать новую заметку!', callback_data = '1')
button_my = InlineKeyboardButton('Мои заметки', callback_data = '2')
button_share = InlineKeyboardButton('Поделиться заметкой', callback_data = '3')
button_del = InlineKeyboardButton('Удалить заметку', callback_data = '4')
button_ch = InlineKeyboardButton('Изменить заметку', callback_data = '5')


help_kb = InlineKeyboardMarkup()
help_kb.add(button_make).add(button_share).add(button_my).add(button_del).add(button_ch)
