from backend.database import execute_query


async def insert_job_offer(user_id: int, country: str, city: str, work_mode: str,
                           experience_required: str, specialization_id: int, salary: int, description: str):
    query = """
            INSERT INTO job_offers (user_id, country, city, work_mode, experience_required, 
                                    specialization_required_id, salary, description)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
    await execute_query(query, (user_id, country, city, work_mode, experience_required,
                                specialization_id, salary, description), fetch_type="none")


async def select_job_offer_by_id(offer_id: int):
    query = """
            SELECT u.first_name, u.last_name,
                   e.company_name,
                   o.country, o.city, o.work_mode, o.experience_required,
                   s.specialization_name, o.salary, o.description, o.created_at
            FROM job_offers o
            INNER JOIN employers e ON o.user_id = e.user_id
            INNER JOIN users u ON e.user_id = u.user_id
            INNER JOIN specializations s ON o.specialization_required_id = s.specialization_id
            WHERE o.offer_id = %s
        """
    return await execute_query(query, (offer_id,), fetch_type="one")


async def select_all_job_offers():
    query = """
            SELECT o.offer_id, o.user_id, o.country, o.city, o.work_mode, o.experience_required, 
                   s.specialization_name, o.salary, o.description, o.created_at
            FROM job_offers o
            INNER JOIN specializations s ON o.specialization_required_id = s.specialization_id
        """
    return await execute_query(query, fetch_type="all")


async def select_job_offer_by_user_id(user_id: int):
    query = """
            SELECT o.offer_id, s.specialization_name
            FROM job_offers o
            INNER JOIN specializations s ON o.specialization_required_id = s.specialization_id
            WHERE o.user_id = %s
        """
    return await execute_query(query, (user_id,), fetch_type="all")


async def update_job_offer_description(offer_id: int, new_description: str):
    query = """
            UPDATE job_offers
            SET description = %s
            WHERE offer_id = %s
        """
    await execute_query(query, (new_description, offer_id), fetch_type="none")


async def delete_job_offer(offer_id: int):
    query = "DELETE FROM job_offers WHERE offer_id = %s"
    await execute_query(query, (offer_id,), fetch_type="none")


async def delete_all_job_offers_by_user_id(user_id: int):
    query = "DELETE FROM job_offers WHERE user_id = %s"
    await execute_query(query, (user_id,), fetch_type="none")


async def select_all_specializations():
    query = "SELECT specialization_name FROM specializations"
    return await execute_query(query, fetch_type="all")


async def select_user_id_by_offer_id(offer_id: int):
    query = "SELECT user_id from job_offers WHERE offer_id = %s"
    return await execute_query(query, (offer_id,), fetch_type="one")


async def select_matching_job_offers(application_id: int):
    query = """
        SELECT
            jo.offer_id, 
            jo.country, 
            jo.city, 
            jo.work_mode, 
            jo.experience_required, 
            s.specialization_name,
            e.company_name,
            jo.salary, 
            jo.description, 
            jo.created_at
        FROM job_offers AS jo
        INNER JOIN applications AS app 
            ON jo.country = app.country 
            AND jo.city = app.city
            AND jo.work_mode = app.work_mode
            AND jo.experience_required = app.experience_level
            AND jo.specialization_required_id = app.specialization_id
        INNER JOIN specializations AS s 
            ON jo.specialization_required_id = s.specialization_id
        INNER JOIN employers AS e 
            ON jo.user_id = e.user_id    
        LEFT JOIN likes AS l 
            ON l.offer_id = jo.offer_id 
            AND l.application_id = app.application_id
        WHERE l.offer_id IS NULL
            AND app.application_id = %s 
        ORDER BY jo.created_at ASC;
    """
    return await execute_query(query, (application_id,), fetch_type="all")
