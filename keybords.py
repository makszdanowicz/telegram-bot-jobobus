from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Employee'),
                                               KeyboardButton(text='Employer')],
                                              [KeyboardButton(text='How bot works and FAQ')]],
                                    resize_keyboard=True,
                                    input_field_placeholder='Choose your role...')


