from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from . import employer_keyboards as kb
from .employer_states import EmployerRegistrationState, AddJobOfferState, ViewEmployerOffers

employer_router = Router()
specializations = []

### Registration Handlers

@employer_router.message(EmployerRegistrationState.email)
async def read_email(message: Message, state: FSMContext):
    email = message.text
    if '@' not in email or '.' not in email or len(email) > 254:
        await message.answer("Invalid email format. Please try again.")
        return

    await state.update_data(email=email)
    # await message.answer(f"Your email: {email}")
    await state.set_state(EmployerRegistrationState.company)
    await message.answer("Enter your company name:")

@employer_router.message(EmployerRegistrationState.company)
async def read_company_name(message: Message, state: FSMContext):
    company = message.text
    if len(company) < 2 or not company.isalnum() and len(company) > 30:
        await message.answer("Company name is too short or too long. Please try again")
        return
    await state.update_data(company=company)

    data = await state.get_data()
    await message.answer(
        f"Your profile has been created:\n"
        f"Company Name: {data['company']}\n"
        f"Email: {data['email']}",
        reply_markup=kb.employer_menu_keyboard
    )
    await state.clear()

### Menu Handlers

@employer_router.message(F.text == 'View employer profile')
async def cmd_view_profile(message: Message):
    await message.answer(
        "Your profile:\n"
        "Company Name: Example Company\n"
        "Email: example@example.com\n"
        "Active Job Offers: number from DB"
    )

@employer_router.message(F.text == 'Offers menu')
async def cmd_offers_menu(message: Message):
    await message.answer("Select an action:", reply_markup=kb.job_offer_menu_keyboard)

@employer_router.message(F.text == 'Create job offer')
async def start_create_offer(message: Message, state: FSMContext):
    await message.answer("Enter the country for the job offer (for example Poland):")
    await state.set_state(AddJobOfferState.country)

@employer_router.message(AddJobOfferState.country)
async def add_country(message: Message, state: FSMContext):
    country = message.text
    if len(country) < 2 or not country.isalnum() and len(country) > 60: # 56 is max for The United Kingdom of Great Britain and Northern Ireland 
        await message.answer("Invalid country name. Please enter a valid country.")
        return
    await state.update_data(country=country)
    await message.answer("Enter the city for the job offer (for example Wroclaw)")
    await state.set_state(AddJobOfferState.city)

@employer_router.message(AddJobOfferState.city)
async def add_city(message: Message, state: FSMContext):
    city = message.text
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
async def finalize_job_offer(message: Message, state: FSMContext):
    description = message.text
    # Verify the length of the description
    min_len = 10 #change to 100 for production
    if len(description) < min_len or len(description) > 1000:
        await message.answer(
            "The job description must be between 100 and 1000 characters. Please try again."
        )
        return
    await state.update_data(description=description)

    data = await state.get_data()
    await message.answer(
        "Job Offer Created Successfully!\n"
        f"Country: {data['country']}\n"
        f"City: {data['city']}\n"
        f"Work Mode: {data['work_mode']}\n"
        f"Experience Level: {data['experience_level']}\n"
        f"Specialization: {data['specialization']}\n"
        f"Description: {data['description']}",
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
        "Description: Example job description."
    )

@employer_router.message(F.text == 'Edit job offer')
async def cmd_edit_offer(message: Message):
    await message.answer("Feature to edit job offers coming soon!")

@employer_router.message(F.text == 'Delete job offer')
async def cmd_delete_offer(message: Message):
    await message.answer("Feature to delete job offers coming soon!")
