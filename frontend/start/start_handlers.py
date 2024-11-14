from aiogram import types, F, Router
from aiogram.types import Message,CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from . import start_keybords as kb

router = Router()


class UserRegistrationStates(StatesGroup):
    name = State()
    surname = State()
    role = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Hello, I'm JobOBus bot!", reply_markup=kb.profile)


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer("You typed a help button")


@router.callback_query(F.data == "create_profile_button")
async def create_profile(callback: CallbackQuery):
    await callback.message.edit_reply_markup()  # usuwa klawiature
    await callback.message.answer('Please, enter command /register')


@router.message(Command('register'))
async def registrate(message: Message, state: FSMContext):
    await state.set_state(UserRegistrationStates.name)
    await message.answer("Type your name: ")


# lowim nie komande, a stan
@router.message(UserRegistrationStates.name)
async def read_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    data_name = await state.get_data()
    await state.set_state(UserRegistrationStates.surname)
    await message.answer(f"Nice to meet you {data_name['name']}! Type your surname:")


@router.message(UserRegistrationStates.surname)
async def read_surname(message: Message, state: FSMContext):
    await state.update_data(surname=message.text)
    await state.set_state(UserRegistrationStates.role)
    await message.answer("Choose your role", reply_markup=kb.role_chooser)


@router.callback_query(UserRegistrationStates.role)
async def read_role(callback: CallbackQuery, state: FSMContext):
    # Sprawdzamy, który przycisk został naciśnięty
    if callback.data == 'employee_button':
        await state.update_data(role='Employee')
    elif callback.data == 'employer_button':
        await state.update_data(role='Employer')

    # Pobieramy zapisane dane z FSMContext
    data = await state.get_data()

    await callback.message.edit_reply_markup() # usuwa klawiature

    # Odpowiadamy użytkownikowi z podsumowaniem profilu
    await callback.message.answer(
        f"Your profile has been created, your bio:\n"
        f"Name: {data['name']}\n"
        f"Surname: {data['surname']}\n"
        f"Role: {data['role']}"
    )

    # Czyścimy stan po zakończeniu
    await state.clear()

    # Odpowiadamy na callback, aby usunąć "kółko" przy przycisku
    await callback.answer()


@router.message(F.text == 'Employee')
async def cmd_employee(message: Message):
    await message.answer("You have chosen Employee role!")


@router.message(F.text == 'Employer')
async def cmd_employer(message: Message):
    await message.answer("You have chosen Employer role!")
