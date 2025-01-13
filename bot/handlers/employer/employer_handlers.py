from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import re

from . import employer_keyboards as kb
from .employer_states import EmployerRegistrationState, AddJobOfferState, UpdateEmployerData

from backend.database.employer import *
from backend.database import *

employer_router = Router()
specializations = []

### Registration Handlers

def validate_string(s):
    """
    Validates that a string contains only lowercase letters, spaces, and hyphens.
    
    Args:
        s (str): The input string to validate.
    
    Returns:
        bool: True if valid, False otherwise.
    """
    return bool(re.fullmatch(r'[a-z\s-]+', s))

@employer_router.message(EmployerRegistrationState.company)
async def read_company_name(message: Message, state: FSMContext):
    company = message.text
    if len(company) < 2 or not company.isalnum() and len(company) > 30:
        await message.answer("Company name is too short or too long. Please try again")
        return
    await state.update_data(company=company)
    data = await state.get_data()

    user_id = message.from_user.id
    company = data.get('company')

    await insert_employer(user_id, company)
    await message.answer(
        f"Your profile has been created:\n"
        f"Company Name: {data['company']}",
        reply_markup=kb.employer_menu_keyboard
    )
    await state.clear()

### Menu Handlers

# @employer_router.message(F.text == 'View employer profile')
# async def cmd_view_profile(message: Message):
#     await message.answer(
#         "Your profile:\n"
#         "Company Name: Example Company\n"
#         "Active Job Offers: number from DB"
#     )


@employer_router.message(F.text == 'View employer profile')
async def cmd_view_profile(message: Message):
    user_id = message.from_user.id
    employer_data = await select_employer_by_id(user_id)

    if employer_data is None:
        await message.answer("Your employer profile not found.")
        return

    await message.answer(
        f"Your profile bio:\n"
        f"First Name: {employer_data['first_name']}\n"
        f"Last Name: {employer_data['last_name']}\n"
        f"Role: {employer_data['role']}\n"
        f"Company Name: {employer_data['company_name']}"
    )

@employer_router.message(F.text == 'Offers menu')
async def cmd_offers_menu(message: Message):
    await message.answer("Select an action:", reply_markup=kb.job_offer_menu_keyboard)

@employer_router.message(F.text == 'Create job offer')
async def start_create_offer(message: Message, state: FSMContext):
    await message.answer("Enter the country for the job offer (for example Poland):", reply_markup=ReplyKeyboardRemove())
    await state.set_state(AddJobOfferState.country)

@employer_router.message(AddJobOfferState.country)
async def add_country(message: Message, state: FSMContext):
    country = message.text
    country = country.lower()
    if not validate_string(country):
        await message.answer('Use only english alphabet, spaces and "-"')
        return       
    if len(country) < 2 or not country.isalnum() and len(country) > 60: # 56 is max for The United Kingdom of Great Britain and Northern Ireland 
        await message.answer("Invalid country name. Please enter a valid country.")
        return
    await state.update_data(country=country)
    await message.answer("Enter the city for the job offer (for example Wroclaw)")
    await state.set_state(AddJobOfferState.city)

@employer_router.message(AddJobOfferState.city)
async def add_city(message: Message, state: FSMContext):
    city = message.text
    city = city.lower()
    if not validate_string(city):
        await message.answer('Use only english alphabet, spaces and "-"')
        return
    if len(city) < 2 or not city.isalnum() and len(city) > 50: #  Most city names are under 50 characters.
        await message.answer("Invalid city name. Please enter a valid city.")
        return
    await state.update_data(city=city)
    await message.answer("Select the work mode:", reply_markup=kb.work_mode_keyboard)
    await state.set_state(AddJobOfferState.work_mode)

@employer_router.callback_query(AddJobOfferState.work_mode)
async def add_work_mode(callback: CallbackQuery, state: FSMContext):
    work_mode = callback.data.split('_')[0]
    await callback.message.edit_reply_markup()
    await state.update_data(work_mode=work_mode)
    await callback.message.answer(f"Selected mode: {work_mode}")
    await callback.message.answer("Select your candidate experience level:", reply_markup=kb.experience_level_keyboard)
    await state.set_state(AddJobOfferState.experience_level)

@employer_router.callback_query(AddJobOfferState.experience_level)
async def add_experience_level(callback: CallbackQuery, state: FSMContext):
    experience_level = callback.data.split('_')[0]
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
    await callback.message.answer(f"Selected level: {experience_level}")
    await state.set_state(AddJobOfferState.specialization)
    await state.update_data(experience_level=experience_level)
    global specializations
    specializations = [
        "AI/ML", "Sys. Administrator", "Business Analysis", "Architecture", "Backend", "Data", "Design",
        "DevOps", "ERP", "Embedded", "Frontend", "Fullstack", "GameDev", "Mobile", "PM", "Security",
        "Support", "Testing", "Other"
    ]
    specialization_list = "\n- ".join(specializations)
    await callback.message.answer(f"Please select your specialization from the list below and type it in:\n- {specialization_list}")


@employer_router.message(AddJobOfferState.specialization)
async def add_specialization(message: Message, state: FSMContext):
    specialization = message.text
    if specialization not in specializations:
        await message.answer("Enter specialization from the list or type \"Other\"")
        return
    await state.update_data(specialization=specialization)
    await message.answer("Enter the job description in range 100 - 1000 symbols")
    await state.set_state(AddJobOfferState.description)

@employer_router.message(AddJobOfferState.description)
async def add_description(message: Message, state: FSMContext):
    description = message.text
    # Verify the length of the description
    min_len = 10 #change to 100 for production
    if len(description) < min_len or len(description) > 1000:
        await message.answer(
            "The job description must be between 100 and 1000 characters. Please try again."
        )
        return
    await state.update_data(description=description)
    await message.answer("Enter the monthly salary in PLN")
    await state.set_state(AddJobOfferState.salary)
@employer_router.message(AddJobOfferState.salary)
async def add_salary(message: Message, state: FSMContext):
    salary = message.text
    min_val = 0
    max_val = 2147483647 #max_int

    # Check if salary is a valid number
    if not salary.isdigit():
        await message.answer("Salary value is not a valid number.")
        return
    
    salary = int(salary)

    if salary < min_val or salary > max_val:
        await message.answer("Salary value is out of range.")
        return
    await state.update_data(salary=salary)


    data = await state.get_data()
    await message.answer(
        "Job Offer Created Successfully!\n"
        f"Country: {data['country'].capitalize()}\n"
        f"City: {data['city'].capitalize()}\n"
        f"Work Mode: {data['work_mode']}\n"
        f"Experience Level: {data['experience_level']}\n"
        f"Specialization: {data['specialization']}\n"
        f"Description: {data['description']}\n"
        f"Salary: {data['salary']} PLN",

        reply_markup=kb.job_offer_menu_keyboard
    )
    await state.clear()

### Job Offer Viewing Handlers

@employer_router.message(F.text == 'View job offers')
async def cmd_view_offers(message: Message):
    await message.answer("Here are your job offers:", reply_markup=kb.view_offers_menu_keyboard)

@employer_router.callback_query(F.data.startswith('view_offer_'))
async def view_specific_offer(callback: CallbackQuery):
    offer_id = callback.data.split('_')[-1]
    # Fetch job offer details using offer_id from DB or API
    await callback.message.answer(
        f"Job Offer ID: {offer_id}\n"
        "Country: Example Country\n"
        "City: Example City\n"
        "Work Mode: Full-Time\n"
        "Experience Level: Senior\n"
        "Specialization: Developer\n"
        "Description: Example job description\n"
        "Salary: Example salary"
    )

@employer_router.message(F.text == 'Edit job offer')
async def cmd_edit_offer(message: Message):
    await message.answer("Feature to edit job offers coming soon!")

@employer_router.message(F.text == 'Delete job offer')
async def cmd_delete_offer(message: Message):
    await message.answer("Feature to delete job offers coming soon!")

@employer_router.message(F.text == 'Delete job offer')
async def cmd_delete_offer(message: Message):
    await message.answer("Feature to delete job offers coming soon!")

@employer_router.message(F.text == 'View specific offer')
async def specific_offer(message: Message):
    await message.answer("Feature to display specific offers coming soon!")

@employer_router.message(F.text == 'View list of all offers')
async def offer_list(message: Message):
    await message.answer("Feature to display the list of job offers coming soon!")
    for i in range (1, 11):
        await message.answer(f"Sample job offer number {i}")
@employer_router.message(F.text == 'Profile menu')
async def cmd_profile_menu(message: Message):
    await message.answer("You have returned to the profile menu.", reply_markup=kb.employer_menu_keyboard)

# Change values

@employer_router.callback_query(F.data == "change_company_name_button'")
async def update_email(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()  # remove the inline keyboard
    await callback.message.answer("Type your updated company name: ")
    await state.set_state(UpdateEmployerData.change_employer_company_name)


@employer_router.message(UpdateEmployerData.change_employer_company_name)
async def change_company_name(message: Message, state: FSMContext):
    changed_company_name = message.text
    if len(changed_company_name) < 2 or not changed_company_name.isalnum() and len(changed_company_name) > 30:
        await message.answer("New company name is too short or too long. Please try again")
        return  
    await state.update_data(changed_company_name=changed_company_name)
    user_id = message.from_user.id
    updated_data = changed_company_name
    updated_data = await state.get_data()
    await state.clear()
    new_company_name = updated_data.get("changed_company_name")
    await change_employer_company_name(user_id, new_company_name)
    await message.answer(
        f"Your new company: {new_company_name}\n"
        f"You have been successfully updated your profile!"
    )

@employer_router.callback_query(F.data == "change_name_button")
async def update_email(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()  # remove the inline keyboard
    await callback.message.answer("Type your updated name: ")
    await state.set_state(UpdateEmployerData.change_employer_name)

@employer_router.callback_query(F.data == "change_last_name_button")
async def update_email(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()  # remove the inline keyboard
    await callback.message.answer("Type your updated last name: ")
    await state.set_state(UpdateEmployerData.change_employer_last_name)

@employer_router.message(UpdateEmployerData.change_employer_last_name)
async def read_new_last_name(message: Message, state: FSMContext):
    await state.update_data(change_employer_last_name=message.text)
    user_id = message.from_user.id
    updated_data = await state.get_data()
    await state.clear()
    new_last_name = updated_data.get("change_employer_last_name")
    await update_user_last_name(user_id, new_last_name)
    await message.answer("You have been successfully updated your last name!",
                            reply_markup=kb.employer_menu_keyboard)
    await state.clear()
@employer_router.message(UpdateEmployerData.change_employer_name)
async def read_new_first_name(message: Message, state: FSMContext):
    await state.update_data(change_employer_name=message.text)
    user_id = message.from_user.id
    updated_data = await state.get_data()
    await state.clear()
    new_first_name = updated_data.get("change_employer_name")
    await update_user_first_name(user_id, new_first_name)
    await message.answer(f"You have been successfully updated your name!",
                            reply_markup=kb.employer_menu_keyboard)
    await state.clear()

@employer_router.message(F.text == '🗑️')
async def cmd_delete_profile(message: Message):
    user_id = message.from_user.id
    await delete_employer(user_id)
    await delete_user(user_id)
    await message.answer("Your profile has been deleted. Enter /start to create new one.")

@employer_router.message(F.text == 'Edit employer profile')
async def cmd_edit_profile(message: Message):
    # Allow editing in case the user made a typo in their first or last name, email.
    await message.answer("What detail you want to change?", reply_markup=kb.change_data_keyboard)