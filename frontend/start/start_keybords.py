from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Employee'),
                                               KeyboardButton(text='Employer')],
                                              [KeyboardButton(text='How bot works and FAQ')]],
                                    resize_keyboard=True,
                                    input_field_placeholder='Choose your role...')

profile = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Create profile',
                                                                      callback_data="create_profile_button")]])

role_chooser = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Employee', callback_data='employee_button')],
        [InlineKeyboardButton(text='Employer', callback_data='employer_button')]
    ]
)


