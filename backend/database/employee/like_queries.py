from backend.database import get_connection, get_pool, execute_query


async def insert_like(application_id: int, offer_id=int):
    query = "INSERT INTO likes (application_id, offer_id) VALUES (%s, %s)"
    await execute_query(query, (application_id, offer_id), fetch_type="none")


async def select_like_id(application_id: int, offer_id: int):
    query = "SELECT like_id FROM likes WHERE application_id = %s AND offer_id = %s"
    return await execute_query(query, (application_id, offer_id), fetch_type="one")

async def delete_like(like_id: int):
    query = """
    DELETE FROM likes
    WHERE like_id = %s
    """
    await execute_query(query, (like_id,), fetch_type="none")

async def delete_all_likes_by_employer_id(user_id: int):
    query = """
    DELETE FROM likes
    WHERE offer_id IN (
        SELECT offer_id
        FROM job_offers
        WHERE user_id = %s
    );
    """
    await execute_query(query, (user_id,), fetch_type="none")

async def delete_all_likes_by_employee_id(user_id: int):
    query = """
    DELETE FROM likes
    WHERE application_id IN (
        SELECT application_id
        FROM applications
        WHERE user_id = %s
    );
    """
    await execute_query(query, (user_id,), fetch_type="none")
