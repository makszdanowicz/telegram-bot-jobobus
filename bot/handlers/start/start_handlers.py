from aiogram import types, F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from bot.utils.dictionary import *

from . import start_keybords as kb
from bot.handlers.employee import EmployeeRegistrationState
# from bot.handlers.employee.employee_states import EmployeeRegistrationState

start_router = Router()  # a router for handling commands and messages at beginning of using the bot

data = {}  # global variable to store user data temporarily


# Define states for user registration process using finite state machine (FSM)
class UserRegistrationState(StatesGroup):
    name = State()
    surname = State()
    role = State()


# Handler for /start command, sends a welcome message with profile creation options
@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(start_text, reply_markup=kb.profile)
    # await message.answer("Hello, I'm JobOBus bot!", reply_markup=kb.profile)


# Handler for /help command, sends a help message
@start_router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer("You typed a help button")


# Handler for when the user clicks the "Create profile" button
@start_router.callback_query(F.data == "create_profile_button")
async def create_profile(callback: CallbackQuery):
    await callback.message.edit_reply_markup()  # after clicking remove the inline keyboard
    await callback.message.answer('To create a profile please, enter command /create_profile')


# Handler for /register command, initiates the registration process and sets the first state
@start_router.message(Command('create_profile'))
async def registrate(message: Message, state: FSMContext):
    await state.set_state(UserRegistrationState.name)  # set the state to collect the user's name
    await message.answer("Type your name: ")


# Handler for collecting the user's name, we are handle not command, but state!!
@start_router.message(UserRegistrationState.name)
async def read_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)  # store the name in the FSM context
    data_name = await state.get_data()
    await state.set_state(UserRegistrationState.surname)  # move to the next state (surname selection)
    await message.answer(f"Nice to meet you {data_name['name']}! Type your surname:")


# Handler for collecting the user's surname
@start_router.message(UserRegistrationState.surname)
async def read_surname(message: Message, state: FSMContext):
    await state.update_data(surname=message.text)
    await state.set_state(UserRegistrationState.role)  # move to the next state (role selection)
    await message.answer("Choose your role", reply_markup=kb.role_chooser)


# Handler for role selection
@start_router.callback_query(UserRegistrationState.role)
async def read_role(callback: CallbackQuery, state: FSMContext):
    # Check which button the user clicked and store the selected role
    if callback.data == 'employee_button':
        await state.update_data(role='Employee')
        await create_user_profile(state)  # Get the user data from registration and add a new record to db
        await state.set_state(EmployeeRegistrationState.email)
        await callback.message.answer("Enter your email, for your contact bio, for example: example@example.com")
    elif callback.data == 'employer_button':
        await state.update_data(role='Employer')
        # TO DO:
        # getData from UserStateReg and add new Record to users db
        # setState for Employer Company name
        await create_user_profile(state)
        await state.set_state(EmployeeRegistrationState.email)  # change to company name state
        await callback.message.answer("Enter the name of your company/organization")

    await callback.answer()
    await callback.message.edit_reply_markup()  # remove the inline keyboard


async def create_user_profile(state: FSMContext):
    global data
    data = await state.get_data()  # Get the user's data from FSM context
    # TO DO: In future we have to implement logic to add a new record do db


# In future let's get data from database, bot now from data variable
# Handler for viewing the user's profile (shows the stored data)
@start_router.message(F.text == 'View user profile')
async def cmd_view_profile(message: Message):
    await message.answer(
        f"Your profile bio:\n"
        f"Name: {data['name']}\n"
        f"Surname: {data['surname']}\n"
        f"Role: {data['role']}"
    )


# Handler for editing the user's profile (this will be implemented later)
@start_router.message(F.text == 'Edit user profile')
async def cmd_edit_profile(message: Message):
    await message.answer("In future it will make update query to db")


# Handler for deleting the user's profile (this will be implemented later)
@start_router.message(F.text == 'Delete user profile')
async def cmd_delete_profile(message: Message):
    await message.answer("In future it will delete profile from db")


@start_router.message(F.text == 'Employee')
async def cmd_employee(message: Message):
    await message.answer("You have chosen Employee role!")


@start_router.message(F.text == 'Employer')
async def cmd_employer(message: Message):
    await message.answer("You have chosen Employer role!")
