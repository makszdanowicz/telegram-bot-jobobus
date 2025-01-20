from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from . import employer_keyboards as kb
from .employer_states import EmployerRegistrationState, AddJobOfferState, UpdateEmployerData, ViewEmployerOffers

from backend.database.employer import (insert_job_offer, select_job_offer_by_id, update_job_offer_description,
delete_job_offer, select_all_job_offers, select_all_specializations, select_job_offer_by_user_id)
from bot.utils import validate_string_for_tags

job_offers_router = Router()
specializations = []

@job_offers_router.message(F.text == 'Profile menu')
async def cmd_profile_menu(message: Message):
    await message.answer("You have returned to the profile menu.", reply_markup=kb.employer_menu_keyboard)

@job_offers_router.message(F.text == 'Offers menu')
async def cmd_offers_menu(message: Message):
    await message.answer("Select an action:", reply_markup=kb.job_offer_menu_keyboard)

@job_offers_router.message(F.text == 'Create job offer')
async def start_create_offer(message: Message, state: FSMContext):
    await message.answer("Enter the country for the job offer (for example Poland):", reply_markup=ReplyKeyboardRemove())
    await state.set_state(AddJobOfferState.country)

@job_offers_router.message(AddJobOfferState.country)
async def add_country(message: Message, state: FSMContext):
    country = message.text
    country = country.lower()
    if not validate_string_for_tags(country):
        await message.answer('Use only english alphabet, spaces and "-"')
        return       
    if not country.isalnum() and len(country) > 60: # 56 is max for The United Kingdom of Great Britain and Northern Ireland 
        await message.answer("Invalid country name. Please enter a valid country.")
        return
    await state.update_data(country=country)
    await message.answer("Enter the city for the job offer (for example Wroclaw)")
    await state.set_state(AddJobOfferState.city)

@job_offers_router.message(AddJobOfferState.city)
async def add_city(message: Message, state: FSMContext):
    city = message.text
    city = city.lower()
    if not validate_string_for_tags(city):
        await message.answer('Use only english alphabet, spaces and "-"')
        return
    if len(city) < 2 or not city.isalnum() and len(city) > 50: #  Most city names are under 50 characters.
        await message.answer("Invalid city name. Please enter a valid city.")
        return
    await state.update_data(city=city)
    await message.answer("Select the work mode:", reply_markup=kb.work_mode_keyboard)
    await state.set_state(AddJobOfferState.work_mode)

@job_offers_router.callback_query(AddJobOfferState.work_mode)
async def add_work_mode(callback: CallbackQuery, state: FSMContext):
    work_mode = callback.data.split('_')[0]
    await callback.message.edit_reply_markup()
    await state.update_data(work_mode=work_mode)
    await callback.message.answer(f"Selected mode: {work_mode}")
    await callback.message.answer("Select your candidate experience level:", reply_markup=kb.experience_level_keyboard)
    await state.set_state(AddJobOfferState.experience_level)

@job_offers_router.callback_query(AddJobOfferState.experience_level)
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
    specializations = await select_all_specializations()

    # Create a numbered list of specializations
    specialization_list = "\n".join(
        [f"{i + 1}. {specialization['specialization_name']}" for i, specialization in enumerate(specializations)])

    await callback.message.answer(
        f"Please select your specialization from the list below and type the number:\n{specialization_list}"
    )
    await callback.answer()


@job_offers_router.message(AddJobOfferState.specialization)
async def add_specialization(message: Message, state: FSMContext):
    specialization_id = int(message.text)
    if specialization_id > len(specializations):
        await message.answer("Enter specialization number from the list")
        return
    await state.update_data(specialization=specialization_id)
    await message.answer("Enter the job description in range 100 - 1000 symbols")
    await state.set_state(AddJobOfferState.description)

@job_offers_router.message(AddJobOfferState.description)
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

@job_offers_router.message(AddJobOfferState.salary)
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

    user_id = message.from_user.id
    country = data['country']
    city = data['city']
    work_mode = data['work_mode']
    experience_level = data['experience_level']
    specialization_id = data['specialization']
    description = data['description']
    salary = data['salary']
    
    await insert_job_offer(user_id, country, city, work_mode, experience_level, specialization_id, salary, description)
    await message.answer(
        "Job Offer Created Successfully!\n"
        f"Country: {country.capitalize()}\n"
        f"City: {city.capitalize()}\n"
        f"Work Mode: {work_mode}\n"
        f"Experience Level: {experience_level}\n"
        f"Specialization: {specialization_id}\n"
        f"Description: {description}\n"
        f"Salary: {salary} PLN",

        reply_markup=kb.job_offer_menu_keyboard
    )
    await state.clear()

### Job Offer Viewing Handlers

@job_offers_router.message(F.text == 'View job offers')
async def cmd_view_offers(message: Message, state: FSMContext):
    user_id = message.from_user.id

    # Fetch job offers posted by the employer
    job_offers = await select_job_offer_by_user_id(user_id)
    
    if not job_offers:
        await message.answer("You haven't posted any job offers yet.")
        return

    offer_list = "\n".join(
        [f"{offer['specialization_name']} (Offer id = {offer['offer_id']})" for offer in job_offers])

    await message.answer(
        f"Your job offers:\n\n{offer_list}\n\n"
        f"Enter the ID of the job offer you want to view:",
    )
    # Set state to expect a specific job offer ID
    await state.set_state(ViewEmployerOffers.choose_offer)

@job_offers_router.message(ViewEmployerOffers.choose_offer)
async def handle_selected_offer(message: Message, state: FSMContext):
    try:
        offer_id = int(message.text)  # Ensure valid integer input
    except ValueError:
        await message.answer("Invalid input. Please enter a valid job offer ID.")
        return

    # Fetch the job offer details
    offer = await select_job_offer_by_id(offer_id)

    if not offer:
        await message.answer("No job offer found with the given ID. Please try again.")
        return

    # Save the selected offer ID in the state for further actions (edit/delete)
    await state.update_data(offer_id=int(offer_id))

    # Display job offer details with the imported keyboard
    await message.answer(
        f"Job Offer Details:\n\n"
        f"Job Offer ID: {offer_id}\n"
        f"Country: {offer['country']}\n"
        f"City: {offer['city']}\n"
        f"Work Mode: {offer['work_mode']}\n"
        f"Experience Level: {offer['experience_required']}\n"
        f"Specialization: {offer['specialization_name']}\n"
        f"Description: {offer['description']}\n"
        f"Salary: {offer['salary'] or 'Not Specified'}\n"
        f"Posted At: {offer['created_at']}",
        reply_markup=kb.view_offers_menu_keyboard  
    )
    await state.set_state(ViewEmployerOffers.manage_offer)  # Set the next state


@job_offers_router.message(ViewEmployerOffers.manage_offer)
async def manage_job_offer(message: Message, state: FSMContext):
    user_action = message.text
    state_data = await state.get_data()
    offer_id = state_data.get("offer_id")

    if user_action == "Edit job offer":
        await message.answer(f"You selected to edit job offer ID {offer_id}. (feature will be available in the future)",
                            reply_markup=kb.job_offer_menu_keyboard)
        # Here, you can set a new state and implement editing logic
        await state.clear()

    elif user_action == "Delete job offer":
        # Confirm deletion before proceeding
        await message.answer(
            f"Are you sure you want to delete job offer ID {offer_id}?\nType 'yes' to confirm or 'no' to cancel."
        )
        await state.set_state(ViewEmployerOffers.confirm_delete)

    elif user_action == "Offers menu":
        await message.answer("Returning to the offers menu.")
        # Here, implement logic to redirect to the main menu or list of offers
        await state.clear()

    else:
        await message.answer("Invalid option. Please use the buttons to select an action.")


@job_offers_router.message(ViewEmployerOffers.confirm_delete)
async def confirm_delete_offer(message: Message, state: FSMContext):
    user_confirmation = message.text.lower()
    state_data = await state.get_data()
    offer_id = state_data.get("offer_id")

    if user_confirmation == "yes":
        # Perform deletion logic
        await delete_job_offer(offer_id)
        await message.answer(f"Job offer ID {offer_id} has been successfully deleted.",
                            reply_markup=kb.job_offer_menu_keyboard)
        await state.clear()

    elif user_confirmation == "no":
        await message.answer("Deletion cancelled. Returning to the offers menu.")
        await state.set_state(ViewEmployerOffers.manage_offer)

    else:
        await message.answer("Invalid response. Please type 'yes' to confirm or 'no' to cancel.")