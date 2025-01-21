from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from .employer_states import CandidateReview
from . import employer_keyboards as kb
from backend.database.employer import (
    count_unread_likes_for_employer, 
    select_oldest_unread_likes_for_employer,
    change_notification_status, 
    select_candidate_email_by_notification_id, 
    delete_notification
)
from backend.database.employee import delete_like

candidates_router = Router()

@candidates_router.message(F.text == "Start searching for a candidate")
async def cmd_start_candidates_review(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await message.answer("🔍 Searching for candidates...")

    try:
        likes_num_dict = await count_unread_likes_for_employer(user_id)
        likes_num = likes_num_dict.get('read_notification_count', 0)
        likes_num = int(likes_num) if likes_num else 0

        if likes_num > 0:
            await message.answer(f"You have {likes_num} new like(s) on your job offers!")
            candidates = await select_oldest_unread_likes_for_employer(user_id)

            if candidates:
                await state.update_data(candidates=candidates)
                await state.set_state(CandidateReview.reviewing)
                await process_candidate(message, state)
            else:
                await message.answer("No candidates found.", reply_markup=kb.job_offer_menu_keyboard)
                await state.clear()
        else:
            await message.answer("No one has liked your offers yet.", reply_markup=kb.job_offer_menu_keyboard)
            await state.clear()

    except Exception as e:
        print(f"Error: {e}")
        await message.answer("An error occurred while processing likes.", reply_markup=kb.job_offer_menu_keyboard)
        await state.clear()

async def process_candidate(message: Message, state: FSMContext):
    data = await state.get_data()
    candidates = data.get("candidates", [])

    if not candidates:
        await message.answer("All candidates have been reviewed.", reply_markup=kb.job_offer_menu_keyboard)
        await state.clear()
        return

    candidate = candidates.pop(0)  # Get the first candidate and remove it from the list
    await state.update_data(candidates=candidates, current_candidate=candidate)

    candidate_message = candidate.get('message', 'No details available.')
    
    await message.answer(candidate_message, reply_markup=kb.view_likes_menu)

@candidates_router.callback_query(F.data == "like_candidate")
async def handle_like_candidate(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    candidate = data.get("current_candidate")

    if candidate:
        await change_notification_status(candidate["notification_id"])
        candidate_email = await select_candidate_email_by_notification_id(candidate["notification_id"])
        await callback.message.answer(f"Candidate liked! Email: {candidate_email['email']}")

    await process_candidate(callback.message, state)
    await callback.answer()

@candidates_router.callback_query(F.data == "dislike_candidate")
async def handle_dislike_candidate(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    candidate = data.get("current_candidate")

    if candidate:
        await delete_like(candidate["notification_id"])
        await delete_notification(candidate["notification_id"])
        await callback.message.answer("Candidate disliked and record removed.")

    await process_candidate(callback.message, state)
    await callback.answer()

@candidates_router.callback_query(F.data == "back_to_offer_menu")
async def handle_back_to_offer_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("Returning to the offers menu...", reply_markup=kb.job_offer_menu_keyboard)
    await callback.answer()
