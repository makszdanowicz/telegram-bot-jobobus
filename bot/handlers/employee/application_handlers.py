from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from . import employee_keyboards as kb
from .employee_states import ApplicationRegistrationState, ApplicationIdState
from bot.handlers.employer import validate_string

from backend.database.employee import (insert_application, delete_application, select_all_specializations,
                                       select_all_applications_id_with_specialization, select_application_by_id)

application_router = Router()  # a router for handling commands and messages in application menu


@application_router.message(F.text == 'Application menu')
async def cmd_application_menu(message: Message):
    await message.answer(text="You have chosen Application menu", reply_markup=kb.application_menu_keyboard)


@application_router.message(F.text == 'Create application')
async def cmd_create_application(message: Message, state: FSMContext):
    create_application_message = ("To create your job application, I need to gather some details about your "
                                  "preferences and requirements. Please answer the following questions step by step. "
                                  "Let’s get started!")
    await message.answer(text=create_application_message, reply_markup=ReplyKeyboardRemove())
    await state.set_state(ApplicationRegistrationState.country)
    await message.answer("Please enter the name of the country where you are looking for a job (for example Poland).")


@application_router.message(ApplicationRegistrationState.country)
async def read_country(message: Message, state: FSMContext):
    country = message.text
    country = country.lower()
    if not validate_string(country):
        await message.answer('Use only english alphabet, spaces and "-"')
        return
    if not country.isalnum() and len(
            country) > 60:  # 56 is max for The United Kingdom of Great Britain and Northern Ireland
        await message.answer("Invalid country name. Please enter a valid country.")
        return
    await state.update_data(country=country)
    await state.set_state(ApplicationRegistrationState.city)
    await message.answer("Please enter the name of the city where you are searching for a job (for example Warsaw).")


@application_router.message(ApplicationRegistrationState.city)
async def read_city(message: Message, state: FSMContext):
    city = message.text
    city = city.lower()
    if not validate_string(city):
        await message.answer('Use only english alphabet, spaces and "-"')
        return
    if len(city) < 2 or not city.isalnum() and len(city) > 50:  # Most city names are under 50 characters.
        await message.answer("Invalid city name. Please enter a valid city.")
        return
    await state.update_data(city=city)
    await state.set_state(ApplicationRegistrationState.work_mode)
    await message.answer("What is your preferred work mode?", reply_markup=kb.work_mode_keyboard)


@application_router.callback_query(ApplicationRegistrationState.work_mode)
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


@application_router.callback_query(ApplicationRegistrationState.experience_level)
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

    specializations = await select_all_specializations()

    # Create a numbered list of specializations
    specialization_list = "\n".join(
        [f"{i + 1}. {specialization['specialization_name']}" for i, specialization in enumerate(specializations)])

    await callback.message.answer(
        f"Please select your specialization from the list below and type the number:\n{specialization_list}"
    )
    await callback.answer()


@application_router.message(ApplicationRegistrationState.specialization)
async def read_specialization(message: Message, state: FSMContext):
    await state.update_data(specialization=message.text)
    await state.set_state(ApplicationRegistrationState.description)
    await message.answer("Tell us about yourself! Please include the technologies and programming languages you know, "
                         "links to your repositories, and any other relevant details")


@application_router.message(ApplicationRegistrationState.description)
async def read_description(message: Message, state: FSMContext):
    description = message.text

    # Verify the length of the description
    min_len = 10  # change to 100 for production
    if len(description) < min_len or len(description) > 1000:
        await message.answer(
            "The job description must be between 100 and 1000 characters. Please try again."
        )
        return

    await state.update_data(description=description)
    application_data = await state.get_data()
    await state.clear()

    # Insert application data to database
    user_id = message.from_user.id
    country = application_data.get("country")
    city = application_data.get("city")
    work_mode = application_data.get("work_mode")
    experience_level = application_data.get("experience_level")
    specialization_id = application_data.get("specialization")
    description = application_data.get("description")
    await insert_application(user_id, country, city, work_mode, experience_level, specialization_id, description)

    await message.answer("You have been successfully created your application!",
                         reply_markup=kb.application_menu_keyboard)


@application_router.message(F.text == 'View application')
async def cmd_view_application(message: Message, state: FSMContext):
    await message.answer(text="You have clicked view application")
    user_id = message.from_user.id
    applications = await select_all_applications_id_with_specialization(user_id)

    if not applications:
        await message.answer(text="No applications found for your profile.")
        return
    application_list = "\n".join(
        [f"{app['specialization_name']} (Application id = {app['application_id']})" for app in applications])
    await message.answer(
        f"Your applications:\n{application_list}\n\nEnter the ID of the application you want to view:"
    )
    await state.set_state(ApplicationIdState.application_id)
    await state.update_data(isView=True)


@application_router.message(ApplicationIdState.application_id)
async def read_application_id(message: Message, state: FSMContext):
    await state.update_data(application_id=message.text)
    chosen_application = await state.get_data()
    await state.clear()

    application_id = chosen_application.get("application_id")
    is_view = chosen_application.get("isView", False)
    is_edit = chosen_application.get("isEdit", False)
    is_delete = chosen_application.get("isDelete", False)

    if is_delete:
        application_from_db = await select_application_by_id(application_id)
        if not application_from_db:
            await message.answer(text="Application with provided id is not exists.")
            return
        await delete_application(application_id)
        await message.answer(f"Your application with id {application_id} has been deleted.")
        return
    if is_view:
        application_from_db = await select_application_by_id(application_id)
        if not application_from_db:
            await message.answer(text="Application with provided id is not exists.")
            return
        application_details = (
            f"Application ID: {application_id}\n"
            f"First Name: {application_from_db['first_name']}\n"
            f"Last Name: {application_from_db['last_name']}\n"
            f"Email: {application_from_db['email']}\n"
            f"Country: {application_from_db['country']}\n"
            f"City: {application_from_db['city']}\n"
            f"Work Mode: {application_from_db['work_mode']}\n"
            f"Experience Level: {application_from_db['experience_level']}\n"
            f"Specialization: {application_from_db['specialization_name']}\n"
            f"Description: {application_from_db['description']}"
        )
        await message.answer(text=application_details)
        return
    if is_edit:
        await message.answer(f"You are editing application with id {application_id}")
        return


@application_router.message(F.text == 'Edit application')
async def cmd_edit_application(message: Message):
    await message.answer(text="You have clicked edit application option")


@application_router.message(F.text == 'Delete application')
async def cmd_delete_application(message: Message, state: FSMContext):
    await message.answer(text="You have clicked delete application option")
    await message.answer(text="Enter the ID of the application you want to delete:")
    await state.set_state(ApplicationIdState.application_id)
    await state.update_data(isDelete=True)


@application_router.message(F.text == 'Back to profile menu')
async def cmd_profile_menu(message: Message):
    await message.answer("You have returned to the profile menu.", reply_markup=kb.employee_menu_keyboard)


@application_router.message(F.text == 'Start searching')
async def cmd_start_search(message: Message):
    await message.answer(text="You have clicked start searching option", reply_markup=kb.stop_searching_keyboard)


@application_router.message(F.text == 'Stop searching')
async def cmd_start_search(message: Message):
    await message.answer(text="You have clicked stop searching option", reply_markup=kb.application_menu_keyboard)
