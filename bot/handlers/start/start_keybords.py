from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


async def main_kb():
    main_kb_builder = ReplyKeyboardBuilder()
    main_kb_builder.add(KeyboardButton(text='Employee'))
    main_kb_builder.add(KeyboardButton(text='Employer'))
    return main_kb_builder.as_markup(resize_keyboard=True,
                                     input_field_placeholder='Choose your role...',
                                     one_time_keyboard=True)


main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Employee'),
            KeyboardButton(text='Employer')
        ],
        [
            KeyboardButton(text='How bot works and FAQ')
         ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Choose your role...'
)

# Inline keyboard for creating a profile
profile = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Create profile',
                callback_data="create_profile_button"
            )
        ]
    ]
)

# Inline keyboard for selecting the user's role (Employee or Employer)
role_chooser = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Employee', callback_data='employee_button')],
        [InlineKeyboardButton(text='Employer', callback_data='employer_button')]
    ]
)


# Reply keyboard for profile management options (View, Edit, Delete profile)
profile_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='View user profile'),
            KeyboardButton(text='Edit user profile')
        ],
        [
            KeyboardButton(text='Delete user profile')
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Manage your profile...'
)
