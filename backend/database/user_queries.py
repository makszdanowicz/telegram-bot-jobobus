from .db import get_connection, get_pool, execute_query


async def insert_user(user_id: int, first_name: str, last_name: str, role: str):
    # SQL query to insert a new user into the 'users' table
    query = """
           INSERT INTO users (user_id, first_name, last_name, role) 
           VALUES (%s, %s, %s, %s)
       """
    await execute_query(query, (user_id, first_name, last_name, role))


async def update_user_role(user_id: int, role: str):
    query = "UPDATE users SET role = %s WHERE user_id = %s"
    await execute_query(query, (role, user_id), fetch_type="none")


async def update_user_first_name(user_id: int, updated_first_name: str):
    query = "UPDATE users SET first_name = %s WHERE user_id = %s"
    await execute_query(query, (updated_first_name, user_id), fetch_type="none")


async def update_user_last_name(user_id: int, updated_last_name: str):
    query = "UPDATE users SET last_name = %s WHERE user_id = %s"
    await execute_query(query, (updated_last_name, user_id), fetch_type="none")


async def delete_user(user_id: int):
    query = "DELETE FROM users WHERE user_id = %s"
    await execute_query(query, (user_id,), fetch_type="none")


async def select_user_by_id(user_id: int):
    query = "SELECT * FROM users WHERE user_id = %s"
    return await execute_query(query, (user_id,), fetch_type="one")


