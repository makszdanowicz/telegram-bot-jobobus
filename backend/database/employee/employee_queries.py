from backend.database import execute_query


async def insert_employee(user_id: int, email: str):
    query = """
            INSERT INTO employees (user_id, email)
            VALUES (%s, %s)
        """
    await execute_query(query, (user_id, email), fetch_type="none")


async def update_employee_email(user_id: int, updated_email: str):
    query = "UPDATE employees SET email = %s WHERE user_id = %s"
    await execute_query(query, (updated_email, user_id), fetch_type="none")


async def select_employee_by_id(user_id: int):
    query = """
            SELECT u.first_name, u.last_name, u.role, e.email
            FROM users u
            INNER JOIN employees e ON u.user_id = e.user_id
            WHERE u.user_id = %s
        """
    return await execute_query(query, (user_id,), fetch_type="one")


async def delete_employee(user_id: int):
    query = "DELETE FROM employees WHERE user_id = %s"
    await execute_query(query, (user_id,), fetch_type="none")
