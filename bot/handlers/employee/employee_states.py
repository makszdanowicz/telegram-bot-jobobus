from aiogram.fsm.state import StatesGroup, State


class EmployeeRegistrationState(StatesGroup):
    email = State()


class ApplicationRegistrationState(StatesGroup):
    country = State()
    city = State()
    work_mode = State()
    experience_level = State()
    specialization = State()
    description = State()
