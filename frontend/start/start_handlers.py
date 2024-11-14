from aiogram import types, F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from . import start_keybords as kb  # import predefined keyboards for the bot

router = Router()  # initialize a new router for handling commands and messages

user_data = {}  # global variable to store user data temporarily


# Define states for user registration process using finite state machine (FSM)
class UserRegistrationStates(StatesGroup):
    name = State()
    surname = State()
    role = State()


# Handler for /start command, sends a welcome message with profile creation options
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Hello, I'm JobOBus bot!", reply_markup=kb.profile)


# Handler for /help command, sends a help message
@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer("You typed a help button")


# Handler for when the user clicks the "Create profile" button
@router.callback_query(F.data == "create_profile_button")
async def create_profile(callback: CallbackQuery):
    await callback.message.edit_reply_markup()  # after clicking remove the inline keyboard
    await callback.message.answer('Please, enter command /register')


# Handler for /register command, initiates the registration process and sets the first state
@router.message(Command('register'))
async def registrate(message: Message, state: FSMContext):
    await state.set_state(UserRegistrationStates.name)  # set the state to collect the user's name
    await message.answer("Type your name: ")


# Handler for collecting the user's name, we are handle not command, but state!!
@router.message(UserRegistrationStates.name)
async def read_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)  # store the name in the FSM context
    data_name = await state.get_data()
    await state.set_state(UserRegistrationStates.surname)  # move to the next state (surname selection)
    await message.answer(f"Nice to meet you {data_name['name']}! Type your surname:")


# Handler for collecting the user's surname
@router.message(UserRegistrationStates.surname)
async def read_surname(message: Message, state: FSMContext):
    await state.update_data(surname=message.text)
    await state.set_state(UserRegistrationStates.role)  # move to the next state (role selection)
    await message.answer("Choose your role", reply_markup=kb.role_chooser)


# Handler for role selection
@router.callback_query(UserRegistrationStates.role)
async def read_role(callback: CallbackQuery, state: FSMContext):
    # Check which button the user clicked and store the selected role
    if callback.data == 'employee_button':
        await state.update_data(role='Employee')
    elif callback.data == 'employer_button':
        await state.update_data(role='Employer')

    global data
    # Get the user's data from FSM context
    data = await state.get_data()

    await callback.message.edit_reply_markup()  # remove the inline keyboard

    # Send a confirmation message with the user's profile details
    await callback.message.answer("You have been successfully created your profile!", reply_markup=kb.profile_keyboard)
    await callback.answer()

    # Clear the FSM state as the registration process is complete
    await state.clear()


# In future let's get data from database, bot now from data variable
# Handler for viewing the user's profile (shows the stored data)
@router.message(F.text == 'View profile')
async def cmd_view_profile(message: Message):
    await message.answer(
        f"Your profile bio:\n"
        f"Name: {data['name']}\n"
        f"Surname: {data['surname']}\n"
        f"Role: {data['role']}"
    )


# Handler for editing the user's profile (this will be implemented later)
@router.message(F.text == 'Edit profile')
async def cmd_edit_profile(message: Message):
    await message.answer("In future it will make update query to db")


# Handler for deleting the user's profile (this will be implemented later)
@router.message(F.text == 'Delete profile')
async def cmd_delete_profile(message: Message):
    await message.answer("In future it will delete profile from db")


@router.message(F.text == 'Employee')
async def cmd_employee(message: Message):
    await message.answer("You have chosen Employee role!")


@router.message(F.text == 'Employer')
async def cmd_employer(message: Message):
    await message.answer("You have chosen Employer role!")
