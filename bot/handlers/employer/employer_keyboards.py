from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


employer_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='View employer profile'),
            KeyboardButton(text='Edit employer profile'),
        ],
        [
            KeyboardButton(text='Delete employer'),
            KeyboardButton(text='Offers menu'),
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
        ],
        [
            KeyboardButton(text='Back to offers menu')
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

view_likes_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Like", callback_data="like_candidate"),
            InlineKeyboardButton(text="Dislike", callback_data="dislike_candidate")
        ],
        [
            InlineKeyboardButton(text="Back to Offer Menu", callback_data="back_to_offer_menu")
        ]
    ]
)