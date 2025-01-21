from backend.database import get_connection, get_pool, execute_query

async def insert_notification(user_id: int, like_id: int, message: str):
    query = "INSERT INTO notifications (user_id, like_id, message) VALUES (%s, %s, %s)"
    await execute_query(query, (user_id, like_id, message), fetch_type="none")

async def select_all_likes_by_user_id(user_id: int):
    execute_query

async def select_message_by_notification_id(notification_id: int):
    execute_query

async def select_candidate_email_by_like_id(like_id: int):
    execute_query