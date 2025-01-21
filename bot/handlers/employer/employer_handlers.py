from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from backend.database.employer.job_offers_queries import delete_all_job_offers_by_user_id

from . import employer_keyboards as kb
from .employer_states import EmployerRegistrationState, AddJobOfferState, UpdateEmployerData

from backend.database.employee import delete_all_likes_by_employer_id
from backend.database.employer import insert_employer, change_employer_company_name, delete_employer, select_employer_by_id, delete_all_notifications_by_user_id
from backend.database import delete_user, update_user_first_name, update_user_last_name
from bot.utils import validate_string_for_tags

employer_router = Router()

### Registration Handlers

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
        reply_markup = kb.employer_menu_keyboard
    )
    await state.set_state(AddJobOfferState.profile_menu)

### Menu Handlers

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

# Change values

@employer_router.callback_query(F.data == "change_company_name_button")
async def update_company(callback: CallbackQuery, state: FSMContext):
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
async def update_name(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()  # remove the inline keyboard
    await callback.message.answer("Type your updated name: ")
    await state.set_state(UpdateEmployerData.change_employer_name)

@employer_router.callback_query(F.data == "change_last_name_button")
async def update_last_name(callback: CallbackQuery, state: FSMContext):
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
async def read_new_name(message: Message, state: FSMContext):
    await state.update_data(change_employer_name=message.text)
    user_id = message.from_user.id
    updated_data = await state.get_data()
    await state.clear()
    new_first_name = updated_data.get("change_employer_name")
    await update_user_first_name(user_id, new_first_name)
    await message.answer(f"You have been successfully updated your name!",
                            reply_markup=kb.employer_menu_keyboard)
    await state.clear()

@employer_router.message(F.text == 'Delete employer')
async def employer_delete_profile(message: Message):
    user_id = message.from_user.id
    await delete_all_notifications_by_user_id(user_id)
    await delete_all_likes_by_employer_id(user_id)
    await delete_all_job_offers_by_user_id(user_id)
    await delete_employer(user_id)
    await delete_user(user_id)
    await message.answer("Your profile has been deleted. Enter /start to create new one.")

@employer_router.message(F.text == 'Edit employer profile')
async def cmd_edit_profile(message: Message):
    # Allow editing in case the user made a typo in their first or last name or company.
    await message.answer("What detail you want to change?", reply_markup=kb.change_data_keyboard)