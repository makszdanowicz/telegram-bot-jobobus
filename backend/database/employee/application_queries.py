from backend.database import get_connection, get_pool, execute_query


async def insert_application(user_id: int, country: str, city: str, work_mode: str, experience_level: str,
                             specialization_id: int, description: str):
    query = """
            INSERT INTO applications (user_id, country, city, work_mode, experience_level, specialization_id, description)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
    await execute_query(query, (user_id, country, city, work_mode, experience_level,
                                specialization_id, description), fetch_type="none")


async def select_all_specializations():
    query = "SELECT specialization_name FROM specializations"
    return await execute_query(query, (), fetch_type="all")


async def select_all_applications_id_with_specialization(user_id: int):
    query = """
            SELECT a.application_id, s.specialization_name
            FROM applications a
            INNER JOIN specializations s ON a.specialization_id = s.specialization_id
            WHERE a.user_id = %s
        """
    return await execute_query(query, (user_id,),fetch_type="all")


async def select_application_by_id(application_id: int):
    query = """
            SELECT u.first_name, u.last_name,
            e.email,
            a.country, a.city, a.work_mode, a.experience_level,
            s.specialization_name, a.description
            FROM applications a
            INNER JOIN employees e ON a.user_id = e.user_id
            INNER JOIN users u ON e.user_id = u.user_id
            INNER JOIN specializations s ON a.specialization_id = s.specialization_id
            WHERE a.application_id = %s
        """
    return await execute_query(query, (application_id,), fetch_type="one")


async def delete_application(application_id: int):
    query = "DELETE FROM applications WHERE application_id = %s"
    await execute_query(query, (application_id,), fetch_type="none")

