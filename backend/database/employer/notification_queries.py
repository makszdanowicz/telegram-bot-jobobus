from backend.database import get_connection, get_pool, execute_query


async def insert_notification(user_id: int, like_id: int, message: str):
    query = "INSERT INTO notifications (user_id, like_id, message) VALUES (%s, %s, %s)"
    await execute_query(query, (user_id, like_id, message), fetch_type="none")
