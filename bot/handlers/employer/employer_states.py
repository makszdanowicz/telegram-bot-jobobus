from aiogram.fsm.state import StatesGroup, State


class EmployerRegistrationState(StatesGroup):
    company = State()

class ViewEmployerOffers(StatesGroup):
    display_offers = State()
    choose_offer = State()
    offers_menu = State()

class AddJobOfferState(StatesGroup):
    country = State()
    city = State()
    work_mode = State()
    experience_level = State()
    specialization = State()
    description = State()
    salary = State()
    profile_menu = State()


class UpdateEmployerData(StatesGroup):
    change_employer_company_name = State()
    change_employer_name = State()
    change_employer_last_name = State()

class UpdateJobOfferState(StatesGroup):
    offer_id = State()
    change_country = State()
    change_city = State()
    change_work_mode = State()
    change_experience_level = State()
    change_specialization = State()
    change_description = State()
    change_salary = State()