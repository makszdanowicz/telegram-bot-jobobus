from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from . import employee_keyboards as kb
from .employee_states import EmployeeRegistrationState, ApplicationRegistrationState, EmployeeUpdateDateState
from bot.utils import validate_string

from backend.database.employee import insert_employee, update_employee_email, delete_employee, select_employee_by_id
from backend.database import delete_user, update_user_first_name, update_user_last_name

employee_router = Router()  # a router for handling commands and messages from employee users
specializations = []  # specializations for application


# Handler for collecting employee's email
@employee_router.message(EmployeeRegistrationState.email)
async def read_email(message: Message, state: FSMContext):
    email = message.text
    if '@' not in email or '.' not in email or len(email) > 254:  # Validation for correct email format
        await message.answer("Invalid email format. Please try again.")
        return

    await state.update_data(email=email)
    data = await state.get_data()

    user_id = message.from_user.id
    email = data.get("email")

    # Insert employee data to database
    await insert_employee(user_id, email)
    await message.answer(
        f"Your email: {data['email']}\n"
        f"You have been successfully created your profile!",
        reply_markup=kb.employee_menu_keyboard
    )

    await state.clear()


@employee_router.message(F.text == 'View employee profile')
async def cmd_view_profile(message: Message):
    user_id = message.from_user.id
    employee_data = await select_employee_by_id(user_id)

    if employee_data is None:
        await message.answer("Your employee profile not found.")
        return

    await message.answer(
        f"Your profile bio:\n"
        f"First Name: {employee_data['first_name']}\n"
        f"Last Name: {employee_data['last_name']}\n"
        f"Role: {employee_data['role']}\n"
        f"Email: {employee_data['email']}"
    )


@employee_router.message(F.text == 'Edit employee profile')
async def cmd_edit_profile(message: Message):
    # Allow editing in case the user made a typo in their first or last name, email.
    await message.answer("What detail you want to change?", reply_markup=kb.parameters_to_update_keyboard)


@employee_router.callback_query(F.data == "first_name_to_update_button")
async def update_first_name(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()  # remove the inline keyboard
    await callback.message.answer("Type your updated name: ")
    await state.set_state(EmployeeUpdateDateState.first_name_to_update)


@employee_router.message(EmployeeUpdateDateState.first_name_to_update)
async def read_new_first_name(message: Message, state: FSMContext):
    await state.update_data(first_name_to_update=message.text)
    user_id = message.from_user.id
    updated_data = await state.get_data()
    await state.clear()
    new_first_name = updated_data.get("first_name_to_update")
    await update_user_first_name(user_id, new_first_name)
    await message.answer("You have been successfully updated your name!")


@employee_router.callback_query(F.data == "last_name_to_update_button")
async def update_last_name(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()  # remove the inline keyboard
    await callback.message.answer("Type your updated last name: ")
    await state.set_state(EmployeeUpdateDateState.last_name_to_update)


@employee_router.message(EmployeeUpdateDateState.last_name_to_update)
async def read_new_last_name(message: Message, state: FSMContext):
    await state.update_data(last_name_to_update=message.text)
    user_id = message.from_user.id
    updated_data = await state.get_data()
    await state.clear()
    new_last_name = updated_data.get("last_name_to_update")
    await update_user_last_name(user_id, new_last_name)
    await message.answer("You have been successfully updated your last name!")


@employee_router.callback_query(F.data == "email_to_update_button")
async def update_email(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()  # remove the inline keyboard
    await callback.message.answer("Type your updated email: ")
    await state.set_state(EmployeeUpdateDateState.email_to_update)


@employee_router.message(EmployeeUpdateDateState.email_to_update)
async def read_new_email(message: Message, state: FSMContext):
    email_to_update = message.text
    if '@' not in email_to_update or '.' not in email_to_update or len(email_to_update) > 254:  # Validation for
        # correct email format
        await message.answer("Invalid email format. Please try again.")
        return
    await state.update_data(email_to_update=email_to_update)
    user_id = message.from_user.id
    updated_data = await state.get_data()
    await state.clear()
    new_email = updated_data.get("email_to_update")
    await update_employee_email(user_id, new_email)
    await message.answer(
        f"Your new email: {new_email}\n"
        f"You have been successfully updated your profile!"
    )


@employee_router.message(F.text == '🗑️')
async def cmd_delete_profile(message: Message):
    user_id = message.from_user.id
    await delete_employee(user_id)
    await delete_user(user_id)
    await message.answer("Your profile has been deleted. Enter /start to create new one.")



# @employee_router.message(F.text == 'Back to profile menu')
# async def cmd_profile_menu(message: Message):
#     await message.answer("You have returned to the profile menu.", reply_markup=kb.employee_menu_keyboard)
