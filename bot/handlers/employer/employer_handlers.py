from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext


from . import employer_keyboards as kb
from .employer_states import EmployerRegistrationState, AddJobOfferState

employer_router = Router()


@employer_router.message(EmployerRegistrationState.email)
async def read_email(message: Message, state: FSMContext):
    email = message.text
    print("bimba")
    if '@' not in email or '.' not in email:  # Validation for correct email format
        await message.answer("Invalid email format. Please try again.")
        return

    await state.update_data(email=email)
    data = await state.get_data()
    await message.answer(
        f"Your email: {data['email']}"
    )
    await state.clear()

@employer_router.message(EmployerRegistrationState.company)
async def read_company_name(message: Message, state: FSMContext):
    company = message.text

    await state.update_data(company=company)
    data = await state.get_data()

    await message.answer(
        f"Your company name is: {data['company']}\n"
        f"You have successfully created your profile!",
        reply_markup=kb.employer_menu_keyboard
    )
    await state.clear()

@employer_router.message(F.text == 'View employer profile')
async def cmd_view_profile(message: Message):
    await message.answer(
        f"Your profile bio:\n"
        f"Company name:\n" 
        f"email: email from DB(Employee)"
    )