from backend.database import get_connection, get_pool, execute_query


async def insert_like(application_id: int, offer_id=int):
    query = "INSERT INTO likes (application_id, offer_id) VALUES (%s, %s)"
    await execute_query(query, (application_id, offer_id), fetch_type="none")


async def select_like_id(application_id: int, offer_id: int):
    query = "SELECT like_id FROM likes WHERE application_id = %s AND offer_id = %s"
    return await execute_query(query, (application_id, offer_id), fetch_type="one")
