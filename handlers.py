from aiogram import types, F,  Router
from aiogram.filters import CommandStart, Command

import keybords as kb

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Hello, I'm JobOBus bot!", reply_markup=kb.main_keyboard)

@router.message(Command('help'))
async def cmd_help(message: types.Message):
    await message.answer("You typed a help button")

@router.message(F.text == 'Employee')
async def cmd_employee(message: types.Message):
    await message.answer("You have chosen Employee role!")

@router.message(F.text == 'Employer')
async def cmd_employer(message: types.Message):
    await message.answer("You have chosen Employer role!")