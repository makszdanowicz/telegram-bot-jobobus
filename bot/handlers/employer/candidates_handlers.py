from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from .employer_states import SearchForCandidate
from . import employer_keyboards as kb
from backend.database.employer import (count_unread_likes_for_employer, select_oldest_unread_likes_for_employer,
    change_notification_status, select_candidate_email_by_notification_id, delete_notification)
from backend.database.employee import delete_like
candidates_router = Router()

@candidates_router.message(F.text == "Start searching for a candidate")
async def cmd_start_candidates_review(message: Message, state: FSMContext):

    user_id = message.from_user.id
    likes_num = await count_unread_likes_for_employer(user_id)
    likes_num = int(likes_num) if likes_num else 0

    if likes_num != 0:
        await message.answer(f"You job offers were liked {likes_num} times!")
        await state.set_state(SearchForCandidate.searching_menu)

    elif likes_num == 0:
        await message.answer(f"It seems that no one liked your offers yet",
                                    reply_markup = kb.job_offer_menu_keyboard)
        await state.clear()

    else:
        await message.answer(f"Error occurred while reading likes number",
                                    reply_markup = kb.job_offer_menu_keyboard)
        await state.clear()

@candidates_router.message(SearchForCandidate.searching_menu)
async def cmd_handle_candidates_likes_menu(message: Message, callback: CallbackQuery, state: FSMContext):
    await message.answer("You are in the search menu.")
    
    user_id = message.from_user.id
    
    candidates = await select_oldest_unread_likes_for_employer(user_id)
    
    # Iterate through candidate applications
    for candidate in candidates:
        candidate_message = candidate["message"]
        
        await message.answer(candidate_message, reply_markup=kb.view_likes_menu)
        
        # Handle user actions with the inline keyboard
        @candidates_router.callback_query(lambda cb: cb.data in ["like_candidate", "dislike_candidate", "back_to_offer_menu"])
        async def handle_candidate_action(callback_query: CallbackQuery):
            action = callback.data
            
            if action == "like_candidate":
                # Mark the notification as "read"
                await change_notification_status(candidate["notification_id"])

                # Retrieve the candidate's email
                candidate_email = await select_candidate_email_by_notification_id(candidate["notification_id"])
                await callback_query.message.answer(f"Candidate liked! Email: {candidate_email}")
            
            elif action == "dislike_candidate":
                await delete_like(candidate["like_id"])
                await delete_notification(candidate["notification_id"])
                await callback_query.message.answer("Candidate disliked and record removed.")
            
            elif action == "back_to_offer_menu":
                # Clear the state and display the job offer menu
                await state.clear()
                await callback_query.message.answer("Returning to the offers menu...", reply_markup=kb.job_offer_menu_keyboard)
            
            await callback_query.answer()
