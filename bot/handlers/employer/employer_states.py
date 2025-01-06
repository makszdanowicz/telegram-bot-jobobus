from aiogram.fsm.state import StatesGroup, State


class EmployerRegistrationState(StatesGroup):
    email = State()
    company = State()

class AddJobOfferState(StatesGroup):
    country = State()
    city = State()
    work_mode = State()
    experience_level = State()
    specialization = State()
    description = State()
