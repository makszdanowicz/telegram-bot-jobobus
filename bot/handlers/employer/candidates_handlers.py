from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from .employer_states import SearchForCandidate
from backend.database.employer import (select_all_likes_by_user_id, select_message_by_notification_id,
    select_candidate_email_by_like_id)
candidates_router = Router()

@candidates_router.message(F.text == "Start searching for a candidate")
async def cmd_start_candidates_review(message: Message, callback: CallbackQuery, state: FSMContext):

    user_id = message.from_user.id
    likes_num = len(await select_all_likes_by_user_id(user_id))
    if likes_num != 0:
        await callback.message.answer(f"You job offers were liked {likes_num} times!")
        await state.set_state(SearchForCandidate.searching_menu)
    elif likes_num == 0:
        await callback.message.answer(f"No one liked your offers yet")
        await state.set_state(SearchForCandidate.searching_menu)
    else:
        await callback.message.answer(f"Error occurred while reading likes number")
        await state.set_state(SearchForCandidate.searching_menu)
        



    # you have n new likes
    # Menu:
    # 1. View likes
    # 2, Back to main menu
@candidates_router.message(SearchForCandidate.searching_menu)