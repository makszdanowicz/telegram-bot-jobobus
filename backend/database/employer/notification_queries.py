from backend.database import get_connection, get_pool, execute_query

async def insert_notification(user_id: int, like_id: int, message: str):
    query = "INSERT INTO notifications (user_id, like_id, message) VALUES (%s, %s, %s)"
    await execute_query(query, (user_id, like_id, message), fetch_type="none")

async def count_unread_likes_for_employer(user_id: int):
    query = """
        SELECT 
            COUNT(n.notification_id) AS unread_like_count
        FROM 
            job_offers jo
        INNER JOIN 
            likes l ON jo.offer_id = l.offer_id
        INNER JOIN 
            notifications n ON l.like_id = n.like_id
        WHERE 
            jo.user_id = %s
            AND n.status = 'unread'
    """
    await execute_query(query, (user_id,), fetch_type="one")
    

async def select_oldest_unread_likes_for_employer(user_id: int):
    query = """
    SELECT n.notification_id, n.message, n.created_at
    FROM notifications n
    JOIN likes l ON n.like_id = l.like_id
    JOIN job_offers jo ON l.offer_id = jo.offer_id
    WHERE jo.user_id = %s AND n.status = 'unread'
    ORDER BY n.created_at ASC;
    """
    await execute_query(query, (user_id,), fetch_type="all")

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
    await execute_query(query, (notification_id,), fetch_type="one")

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
