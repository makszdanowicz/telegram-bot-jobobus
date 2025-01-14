from aiogram import types, F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from bot.utils.dictionary import *
from bot.utils import validate_string

from . import start_keybords as kb
from bot.handlers.employer import employer_keyboards as kb_employer
from bot.handlers.employee import employee_keyboards as kb_employee
from bot.handlers.employee import EmployeeRegistrationState
from bot.handlers.employer import EmployerRegistrationState, AddJobOfferState

from backend.database.user_queries import insert_user, select_user_by_id, delete_user, update_user_first_name, \
    update_user_last_name

start_router = Router()  # a router for handling commands and messages at beginning of using the bot

data = {}  # global variable to store user data temporarily


# Define states for user registration process using finite state machine (FSM)
class UserRegistrationState(StatesGroup):
    user_id = State()
    name = State()
    surname = State()
    role = State()


class UpdateUserDataState(StatesGroup):
    updated_first_name = State()
    updated_last_name = State()


# Handler for /start command, sends a welcome message with profile creation options
@start_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_data = await select_user_by_id(user_id)
    if not user_data:
        # If user does not exist, ask them to register
        await message.answer(
            "You are not registered in the system. Please contact support or register through the provided link.",
            reply_markup=kb.profile
        )
        return

    # Check the user's role
    user_role = user_data.get("role")
    if user_role == "employer":
        # Change state to Employer's workflow
        await message.answer(
            "Welcome back, Employer!",
            reply_markup=kb_employer.employer_menu_keyboard
        )
        await state.clear()

    elif user_role == "employee":
        # Change state to Employee's workflow
        await message.answer(
            "Welcome back, Employee!",
            reply_markup=kb_employee.employee_menu_keyboard
        )
        await state.clear()

    else:
        # Handle unknown roles
        await message.answer("Your role is not recognized. Please contact support.")
        await state.clear()

# Handler for /help command, sends a help message
@start_router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer("Enter /start to run bot")


# Handler for when the user clicks the "Create profile" button
@start_router.callback_query(F.data == "create_profile_button")
async def cmd_create_profile(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()  # after clicking remove the inline keyboard
    await state.set_state(UserRegistrationState.user_id)
    user_id = callback.from_user.id
    await state.update_data(user_id=user_id)
    await state.set_state(UserRegistrationState.name)  # set the state to collect the user's name
    await callback.message.answer("Type your name: ")


# Handler for collecting the user's name, we are handle not command, but state!!
@start_router.message(UserRegistrationState.name)
async def read_name(message: Message, state: FSMContext):
    name = message.text.strip()
    if not validate_string(name) or len(name) > 100:
        await message.answer("Use only allowed symbols to enter the name.")
        return
    await state.update_data(name=name)
    await state.set_state(UserRegistrationState.surname)
    await message.answer(f"Nice to meet you {name}! Type your surname:")



# Handler for collecting the user's surname
@start_router.message(UserRegistrationState.surname)
async def read_surname(message: Message, state: FSMContext):
    surname = message.text.strip()
    if not validate_string(surname) or len(surname) > 100:
        await message.answer("Use only allowed symbols to enter the last name.")
        return
    await state.update_data(surname=surname)
    await state.set_state(UserRegistrationState.role)
    await message.answer("Choose your role:", reply_markup=kb.role_chooser)


# Handler for role selection
@start_router.callback_query(UserRegistrationState.role)
async def read_role(callback: CallbackQuery, state: FSMContext):
    # Check which button the user clicked and store the selected role
    if callback.data == 'employee_button':
        await state.update_data(role='employee')
        await create_user_profile(state)  # Get the user data from registration and add a new record to db
        await state.set_state(EmployeeRegistrationState.email)
        await callback.message.answer("Enter your email, for your contact bio, for example: example@example.com")
    elif callback.data == 'employer_button':
        await state.update_data(role='employer')
        await create_user_profile(state)  # getData from UserStateReg and add new Record to users db'
        await state.set_state(EmployerRegistrationState.company)  # change to company name state
        await callback.message.answer("Enter your company name:")
    # await callback.message()
    await callback.message.edit_reply_markup()  # remove the inline keyboard


async def create_user_profile(state: FSMContext):
    global data
    data = await state.get_data()  # Get the user's data from FSM context
    # TO DO: In future we have to implement logic to add a new record do db
    user_id = data.get("user_id")
    first_name = data.get("name")
    last_name = data.get("surname")
    role = data.get("role")
    await insert_user(user_id, first_name, last_name, role)


# Handler for viewing the user's profile (shows the stored data)
@start_router.message(F.text == 'View user profile')
async def cmd_view_profile(message: Message):
    user_id = message.from_user.id
    user_data = await select_user_by_id(user_id)

    if user_data is None:
        await message.answer("Profile not found.")
        return

    await message.answer(
        f"Your profile bio:\n"
        f"Name: {user_data['first_name']}\n"
        f"Surname: {user_data['last_name']}\n"
        f"Role: {user_data['role']}"
    )


# Handler for editing the user's profile (this will be implemented later)
@start_router.message(F.text == 'Edit user profile')
async def cmd_edit_profile(message: Message):
    await message.answer("What detail you want to change?", reply_markup=kb.updated_parameter_keyboard)


@start_router.callback_query(F.data == "first_name_button")
async def update_first_name(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()  # after clicking remove the inline keyboard
    await callback.message.answer("Type your updated name: ")
    await state.set_state(UpdateUserDataState.updated_first_name)


@start_router.message(UpdateUserDataState.updated_first_name)
async def read_new_first_name(message: Message, state: FSMContext):
    await state.update_data(updated_first_name=message.text)
    user_id = message.from_user.id
    updated_data = await state.get_data()
    await state.clear()
    updated_first_name = updated_data.get("updated_first_name")
    await update_user_first_name(user_id, updated_first_name)


@start_router.callback_query(F.data == "last_name_button")
async def update_last_name(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()  # after clicking remove the inline keyboard
    await callback.message.answer("Type your updated last name: ")
    await state.set_state(UpdateUserDataState.updated_last_name)


@start_router.message(UpdateUserDataState.updated_last_name)
async def read_new_first_name(message: Message, state: FSMContext):
    await state.update_data(updated_last_name=message.text)
    user_id = message.from_user.id
    updated_data = await state.get_data()
    await state.clear()
    updated_last_name = updated_data.get("updated_last_name")
    await update_user_last_name(user_id, updated_last_name)


# Handler for deleting the user's profile (this will be implemented later)
@start_router.message(F.text == 'Delete user profile')
async def cmd_delete_profile(message: Message):
    # Deleting user from database
    user_id = message.from_user.id
    await delete_user(user_id)

    await message.answer("Your profile has been deleted. Enter /start to run bot.")

