from aiogram.fsm.state import StatesGroup, State


class EmployerRegistrationState(StatesGroup):
    company = State()

class ViewEmployerOffers(StatesGroup):
    display_offers = State()
    choose_offer = State()

class AddJobOfferState(StatesGroup):
    country = State()
    city = State()
    work_mode = State()
    experience_level = State()
    specialization = State()
    description = State()
    salary = State()
