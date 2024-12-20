from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

employee_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='View employee profile'),
            KeyboardButton(text='Edit employee profile'),
            KeyboardButton(text='Delete employee profile')
        ],
        [
            KeyboardButton(text='Application menu')
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Manage your profile...'
)

application_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Create application'),
            KeyboardButton(text='View application'),
        ],
        [
            KeyboardButton(text='Edit application'),
            KeyboardButton(text='Delete application')
        ],
        [
            KeyboardButton(text='Start searching'),
            KeyboardButton(text='Back to profile menu')
        ]
    ]
)
