from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


employer_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='View employer profile'),
            KeyboardButton(text='Edit employer profile'),
            KeyboardButton(text='🗑️') #Delete employer profile
        ],
        [
            KeyboardButton(text='Offers menu')
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Manage your profile...'
)
job_offer_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Create job offer'),
            KeyboardButton(text='View job offers'),
        ],
        [
            KeyboardButton(text='Start searching for a candidate')
        ],
        [
            KeyboardButton(text='Profile menu')
        ]
    ]
)
view_offers_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Edit job offer'),
            KeyboardButton(text='Delete job offer'),
            KeyboardButton(text='View specific offer'),
        ],
        [
            KeyboardButton(text='View list of all offers'),
            KeyboardButton(text='Offers menu')
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

change_data_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='First name', callback_data='change_name_button'),
            InlineKeyboardButton(text='Last name', callback_data='change_last_name_button')
        ],
        [
            InlineKeyboardButton(text='Company name', callback_data='change_company_name_button')
        ]
    ]
)
