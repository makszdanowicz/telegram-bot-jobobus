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


class EmployeeUpdateDateState(StatesGroup):
    first_name_to_update = State()
    last_name_to_update = State()
    email_to_update = State()
