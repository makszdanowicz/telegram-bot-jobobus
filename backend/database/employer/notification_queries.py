from backend.database import get_connection, get_pool, execute_query

async def insert_notification(user_id: int, like_id: int, message: str):
    query = "INSERT INTO notifications (user_id, like_id, message) VALUES (%s, %s, %s)"
    await execute_query(query, (user_id, like_id, message), fetch_type="none")

async def count_unread_likes_for_employer(user_id: int):
    query = """
    SELECT COUNT(n.notification_id) AS read_notification_count
    FROM employers e
    INNER JOIN notifications n ON e.user_id = n.user_id
    WHERE e.user_id = %s AND n.status = 'unread';
    """
    result = await execute_query(query, (user_id,), fetch_type="one")
    print(result)
    return result
    

async def select_oldest_unread_likes_for_employer(user_id: int):
    query = """
    SELECT n.notification_id, n.message, n.created_at FROM notifications as n
    INNER JOIN likes as l ON n.like_id = l.like_id
    INNER JOIN job_offers as jo ON jo.offer_id = l.offer_id
    WHERE n.user_id = %s AND n.status = "unread"
    AND jo.offer_id = l.offer_id
    ORDER BY n.created_at ASC;
    """
    return await execute_query(query, (user_id,), fetch_type="all")

async def change_notification_status(notification_id: int):
    query = """
    UPDATE notifications
    SET status = 'read'
    WHERE notification_id = %s;
    """
    await execute_query(query, (notification_id,), fetch_type="none")

async def select_candidate_email_by_notification_id(notification_id: int):
    query = """
    SELECT e.email
    FROM notifications n
    JOIN likes l ON n.like_id = l.like_id
    JOIN applications a ON l.application_id = a.application_id
    JOIN employees e ON a.user_id = e.user_id
    WHERE n.notification_id = %s;
    """
    return await execute_query(query, (notification_id,), fetch_type="one")

async def delete_notification(notification_id: int):
    query = """
    DELETE FROM notifications
    WHERE notification_id = %s
    """
    await execute_query(query, (notification_id,), fetch_type="none")

async def delete_all_notifications_by_user_id(user_id: int):
    query = """
    DELETE FROM notifications
    WHERE user_id = %s;
    """
    await execute_query(query, (user_id,), fetch_type="none")

async def delete_all_notifications_by_employee_id(user_id: int):
    query = """
    DELETE FROM notifications
    WHERE like_id IN (
        SELECT like_id
        FROM likes
        WHERE application_id IN (
            SELECT application_id
            FROM applications
            WHERE user_id = %s
        )
    );
    """
    await execute_query(query, (user_id,), fetch_type="none")
