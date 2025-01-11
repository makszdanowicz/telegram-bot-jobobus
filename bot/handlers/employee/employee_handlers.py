from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from . import employee_keyboards as kb
from .employee_states import EmployeeRegistrationState, ApplicationRegistrationState

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


@employee_router.message(F.text == '🗑️')
async def cmd_delete_profile(message: Message):
    await message.answer("In future it will delete profile from db")


@employee_router.message(F.text == 'Application menu')
async def cmd_application_menu(message: Message):
    await message.answer(text="You have chosen Application menu", reply_markup=kb.application_menu_keyboard)


@employee_router.message(F.text == 'Create application')
async def cmd_create_application(message: Message, state: FSMContext):
    create_application_message = ("To create your job application, I need to gather some details about your "
                                  "preferences and requirements. Please answer the following questions step by step. "
                                  "Let’s get started!")
    await message.answer(text=create_application_message, reply_markup=ReplyKeyboardRemove())
    await state.set_state(ApplicationRegistrationState.country)
    await message.answer("Please enter the name of the country where you are looking for a job (for example Poland).")


@employee_router.message(ApplicationRegistrationState.country)
async def read_country(message: Message, state: FSMContext):
    await state.update_data(country=message.text)
    await state.set_state(ApplicationRegistrationState.city)
    await message.answer("Please enter the name of the city where you are searching for a job (for example Warsaw).")


@employee_router.message(ApplicationRegistrationState.city)
async def read_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await state.set_state(ApplicationRegistrationState.work_mode)
    await message.answer("What is your preferred work mode?", reply_markup=kb.work_mode_keyboard)


@employee_router.callback_query(ApplicationRegistrationState.work_mode)
async def read_work_mode(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'stationary_button':
        await state.update_data(work_mode='stationary')
    elif callback.data == 'remote_button':
        await state.update_data(work_mode='remote')
    elif callback.data == 'hybrid_button':
        await state.update_data(work_mode='hybrid')
    elif callback.data == 'any_mode_button':
        await state.update_data(work_mode='any')
    await callback.message.edit_reply_markup()  # remove the inline keyboard
    await state.set_state(ApplicationRegistrationState.experience_level)
    await callback.message.answer("Please specify your level of experience", reply_markup=kb.experience_level_keyboard)
    await callback.answer()


@employee_router.callback_query(ApplicationRegistrationState.experience_level)
async def read_experience_level(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'intern_button':
        await state.update_data(experience_level='Intern')
    elif callback.data == 'junior_button':
        await state.update_data(experience_level='Junior')
    elif callback.data == 'mid_button':
        await state.update_data(experience_level='Mid')
    elif callback.data == 'senior_button':
        await state.update_data(experience_level='Senior')
    elif callback.data == 'expert_button':
        await state.update_data(experience_level='Expert')
    await callback.message.edit_reply_markup()  # remove the inline keyboard
    await state.set_state(ApplicationRegistrationState.specialization)
    global specializations
    specializations = [
        "AI/ML", "Sys. Administrator", "Business Analysis", "Architecture", "Backend", "Data", "Design",
        "DevOps", "ERP", "Embedded", "Frontend", "Fullstack", "GameDev", "Mobile", "PM", "Security",
        "Support", "Testing", "Other"
    ]
    specialization_list = "\n- ".join(specializations)
    await callback.message.answer(
        f"Please select your specialization from the list below and type it in:\n- {specialization_list}")
    await callback.answer()


@employee_router.message(ApplicationRegistrationState.specialization)
async def read_specialization(message: Message, state: FSMContext):
    await state.update_data(specialization=message.text)
    await state.set_state(ApplicationRegistrationState.description)
    await message.answer("Tell us about yourself! Please include the technologies and programming languages you know, "
                         "links to your repositories, and any other relevant details")


@employee_router.message(ApplicationRegistrationState.description)
async def read_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    data = state.get_data()
    await state.clear()
    await message.answer("You have been successfully created your application!",
                         reply_markup=kb.application_menu_keyboard)


@employee_router.message(F.text == 'View application')
async def cmd_view_application(message: Message):
    await message.answer(text="You have clicked view application")


@employee_router.message(F.text == 'Edit application')
async def cmd_edit_application(message: Message):
    await message.answer(text="You have clicked edit application option")


@employee_router.message(F.text == 'Delete application')
async def cmd_delete_application(message: Message):
    await message.answer(text="You have clicked delete application option")


@employee_router.message(F.text == 'Start searching')
async def cmd_start_search(message: Message):
    await message.answer(text="You have clicked start searching option", reply_markup=ReplyKeyboardRemove())


@employee_router.message(F.text == 'Back to profile menu')
async def cmd_profile_menu(message: Message):
    await message.answer("You have returned to the profile menu.", reply_markup=kb.employee_menu_keyboard)
