from aiogram.fsm.state import StatesGroup, State


class EmployeeRegistrationState(StatesGroup):
    email = State()
