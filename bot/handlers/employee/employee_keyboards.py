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
            KeyboardButton(text='Job search menu'),
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

parameters_to_update_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='first name', callback_data='first_name_to_update_button'),
            InlineKeyboardButton(text='last name', callback_data='last_name_to_update_button')
        ],
        [
            InlineKeyboardButton(text='email', callback_data='email_to_update_button')
        ]
    ]
)

start_searching_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Start search', callback_data='start_search_job')
        ]
    ]
)

like_dislike_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='👍', callback_data='like_button'),
            InlineKeyboardButton(text='Skip', callback_data='dislike_button')
        ]
    ]
)

stop_searching_button = KeyboardButton(text='Stop searching')
stop_searching_keyboard = ReplyKeyboardMarkup(
    keyboard=[[stop_searching_button]]
)
