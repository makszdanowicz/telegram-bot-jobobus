from aiogram import types, F, Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from . import employee_keybords as kb
from .employee_states import EmployeeRegistrationState

# from bot.handlers.employee.employee_states import EmployeeRegistrationState

employee_router = Router()  # a router for handling commands and messages from employee users


# Handler for collecting employee's email
@employee_router.message(EmployeeRegistrationState.email)
async def read_email(message: Message, state: FSMContext):
    email = message.text
    if '@' not in email or '.' not in email:  # Validation for correct email format
        await message.answer("Invalid email format. Please try again.")
        return

    await state.update_data(email=email)
    data = await state.get_data()

    # TO DO: create_employee_record(data)
    await message.answer(
        f"Your email: {data['email']}\n"
        f"You have been successfully created your profile!",
        reply_markup=kb.employee_menu_keyboard
    )

    await state.clear()


@employee_router.message(F.text == 'View employee profile')
async def cmd_view_profile(message: Message):
    await message.answer(
        f"Your profile bio:\n"
        f"Name: name from DB\n"
        f"Surname: surname from DB\n"
        f"Role: role from DB(Employee)\n"
        f"email: email from DB(Employee)"
    )


@employee_router.message(F.text == 'Edit employee profile')
async def cmd_edit_profile(message: Message):
    # Allow editing in case the user made a typo in their first or last name.
    await message.answer("In future it will make update query to db")


@employee_router.message(F.text == 'Delete employee profile')
async def cmd_delete_profile(message: Message):
    await message.answer("In future it will delete profile from db")


@employee_router.message(F.text == 'Application menu')
async def cmd_application_menu(message: Message):
    await message.answer(text="You have chosen Application menu", reply_markup=kb.application_menu_keyboard)


@employee_router.message(F.text == 'Create application')
async def cmd_create_application(message: Message):
    await message.answer(text="You have clicked create application option", reply_markup=ReplyKeyboardRemove())


@employee_router.message(F.text == 'Edit application')
async def cmd_edit_application(message: Message):
    await message.answer(text="You have clicked edit application option")


@employee_router.message(F.text == 'Delete application')
async def cmd_delete_application(message: Message):
    await message.answer(text="You have clicked delete application option")


@employee_router.message(F.text == 'Start searching')
async def cmd_start_search(message: Message):
    await message.answer(text="You have clicked start searching option", reply_markup=ReplyKeyboardRemove())
