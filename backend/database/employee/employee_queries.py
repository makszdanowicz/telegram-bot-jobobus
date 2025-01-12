import aiomysql
from backend.database import get_connection, get_pool


async def insert_employee(user_id: int, email: str):
    query = """
            INSERT INTO employees (user_id, email)
            VALUES (%s, %s)
        """
    connection = None
    try:
        connection = await get_connection()
        async with connection.cursor() as cursor:
            await cursor.execute(query, (user_id, email))
            print("Employee added successfully.\n")
    except Exception as e:
        print(f"Error while inserting employee: {e}")
    finally:
        if connection:
            pool = await get_pool()
            await pool.release(connection)
            print("Connection released back to the pool.")


async def update_employee_email(user_id: int, updated_email: str):
    query = "UPDATE employees SET email = %s WHERE user_id = %s"
    connection = None
    try:
        connection = await get_connection()
        async with connection.cursor() as cursor:
            await cursor.execute(query, (updated_email, user_id))
            print(f"Employee email updated successfully:{updated_email}\n")
    except Exception as e:
        print(f"Error while updating employee email: {e}")
    finally:
        if connection:
            pool = await get_pool()
            await pool.release(connection)
            print("Connection released back to the pool.")


async def select_employee_by_id(user_id: int):
    query = """
            SELECT u.first_name, u.last_name, u.role, e.email
            FROM users u
            INNER JOIN employees e ON u.user_id = e.user_id
            WHERE u.user_id = %s
        """
    connection = None
    try:
        connection = await get_connection()
        async with connection.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute(query, (user_id,))
            employee_data = await cursor.fetchone()
            return employee_data
    except Exception as e:
        print(f"Error while selecting user: {e}")
        return None
    finally:
        if connection:
            pool = await get_pool()
            await pool.release(connection)
            print("Connection released back to the pool.")


async def delete_employee(user_id: int):
    query = "DELETE FROM employees WHERE user_id = %s"
    connection = None
    try:
        connection = await get_connection()
        async with connection.cursor() as cursor:
            await cursor.execute(query, (user_id,))
            print(f"Employee with id({user_id}) deleted successfully.\n")
    except Exception as e:
        print(f"Error while deleting employee: {e}")
    finally:
        if connection:
            pool = await get_pool()
            await pool.release(connection)
            print("Connection released back to the pool.")