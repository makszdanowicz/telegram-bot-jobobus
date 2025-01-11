from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

employee_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='View employee profile'),
            KeyboardButton(text='Edit employee profile'),
        ],
        [
            KeyboardButton(text='🗑️'),  # Delete employee profile
            KeyboardButton(text='Application menu')
        ]
    ],
    # resize_keyboard=True,
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

work_mode_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='stationary', callback_data='stationary_button'),
            InlineKeyboardButton(text='remote', callback_data='remote_button')
        ],
        [
            InlineKeyboardButton(text='hybrid', callback_data='hybrid_button'),
            InlineKeyboardButton(text='any', callback_data='any_mode_button')
        ]
    ]
)

experience_level_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Intern', callback_data='intern_button'),
            InlineKeyboardButton(text='Junior', callback_data='junior_button')
        ],
        [
            InlineKeyboardButton(text='Mid', callback_data='mid_button'),
            InlineKeyboardButton(text='Senior', callback_data='senior_button'),
        ],
        [
            InlineKeyboardButton(text='Expert', callback_data='expert_button')
        ]
    ]
)
