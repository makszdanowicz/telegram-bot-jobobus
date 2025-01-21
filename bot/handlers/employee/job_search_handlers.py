from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from .employee_states import SearchingJobOfferState
from . import employee_keyboards as kb

from backend.database.employee import insert_like, select_like_id, select_application_by_id
from backend.database.employer import select_user_id_by_offer_id, insert_notification, select_matching_job_offers

searching_job_router = Router()


@searching_job_router.callback_query(F.data == 'start_search_job')
async def match_job_offers(callback_query: CallbackQuery, state: FSMContext):
    # Retrieve the chosen application data from FSMContext
    chosen_application = await state.get_data()
    await state.clear()  # Clear the current state
    application_id = chosen_application.get("application_id")

    # Notify the user that the search has started
    await callback_query.message.answer(
        f"🔎Start looking for job offers for your application with ID {application_id}\n"
        f"If you want to stop searching, click the 'Stop Searching' button in the menu.",
        reply_markup=kb.stop_searching_keyboard)

    # Fetch matching job offers from the database
    # job_offers = None
    job_offers = await select_matching_job_offers(application_id)

    # If no matching offers are found, notify the user
    if not job_offers:
        await callback_query.message.answer("❌ No job offers found for your application.\n"
                                            "Try to create another application.",
                                            reply_markup=kb.application_menu_keyboard)
        return

    # Set the active state to indicate job search is ongoing
    await state.set_state(SearchingJobOfferState.active)

    # Save job offers and related data to FSMContext
    await state.update_data(application_id=application_id, job_offers=job_offers, current_offer_index=0)

    # Send the first job offer to the user
    await send_next_job_offer(callback_query.message, state)


async def send_next_job_offer(message: Message, state: FSMContext):
    # checking is a searching job state is currently active
    current_state = await state.get_state()
    if current_state != SearchingJobOfferState.active.state:
        return

    # Retrieve the current job offers and index from FSMContext
    user_data = await state.get_data()
    job_offers = user_data.get("job_offers", [])
    current_offer_index = user_data.get("current_offer_index")

    # If all job offers have been shown, notify the user
    if current_offer_index >= len(job_offers):
        await message.answer(text="🎉That's all the job offers now! Return to main application menu.",
                             reply_markup=kb.application_menu_keyboard)
        await state.clear()
        return

    current_offer = job_offers[current_offer_index]
    job_text = (
        f"💼 Job Offer Details:\n"
        f"📌 Position: {current_offer['specialization_name']}\n"
        f"🏢 Company: {current_offer['company_name']}\n"
        f"🌍 Location:\n country: {current_offer['country']}\n city: {current_offer['city']}\n"
        f"💰 Salary: {current_offer['salary']} PLN\n\n"
        f"📄 Description:\n{current_offer['description']}"
    )
    await message.answer(text=job_text, reply_markup=kb.like_dislike_keyboard)  # Send the job offer to the user
    await state.update_data(current_offer_index=current_offer_index + 1)  # actualize index of next job offer


@searching_job_router.callback_query(F.data.in_({'like_button', 'dislike_button'}))
async def handle_like_dislike(callback: CallbackQuery, state: FSMContext):
    """
    Handles user interactions with the 'like' and 'dislike' buttons on job offers.
    """
    # Retrieve job search data from FSMContext
    user_data = await state.get_data()
    job_offers = user_data.get("job_offers", [])
    current_offer_index = user_data.get("current_offer_index", 1)
    application_id = user_data.get("application_id")

    # Ensure the current index is valid and within bounds
    if current_offer_index <= len(job_offers):
        current_offer = job_offers[current_offer_index - 1]  # -1 because index was incremented in send_next_job_offer
        offer_id = current_offer['offer_id']
    else:
        return

    if callback.data == 'like_button':
        # Generate like record to db
        await insert_like(application_id, offer_id)

        # Generate a notification message to employer
        receiver_id_from_db = await select_user_id_by_offer_id(offer_id)
        receiver_id = receiver_id_from_db['user_id']

        like_id_from_db = await select_like_id(application_id, offer_id)
        like_id = like_id_from_db['like_id']

        message = await generate_message_for_notification(application_id)
        await callback.message.answer(text=message)

        await insert_notification(receiver_id, like_id, message)

    # Show the next job offer
    await send_next_job_offer(callback.message, state)


async def generate_message_for_notification(application_id: int):
    # Fetch the application details from the database
    application_from_db = await select_application_by_id(application_id)
    if not application_from_db:
        return None

    # Construct the notification message with all the application details
    message = (
        "🔔 **New Application Notification** 🔔\n"
        "Here are the details:\n\n"
        f"👤 First Name: {application_from_db['first_name']}\n"
        f"👤 Last Name: {application_from_db['last_name']}\n"
        f"🌍 Country: {application_from_db['country']}\n"
        f"🏙️ City: {application_from_db['city']}\n"
        f"🖥️ Work Mode: {application_from_db['work_mode']}\n"
        f"📈 Experience Level: {application_from_db['experience_level']}\n"
        f"🛠️ Specialization: {application_from_db['specialization_name']}\n"
        f"📄 Description:\n{application_from_db['description']}\n"
        "\n🚀 Respond to this application!"
    )
    return message


@searching_job_router.message(F.text == 'Stop searching')
async def cmd_stop_search(message: Message, state: FSMContext):
    """
    Handles the 'Stop searching' command to cancel the job search process.
    """
    await state.clear()

    await message.answer(text="🔴 Job search cancelled. Return to main application menu.",
                         reply_markup=kb.application_menu_keyboard)
