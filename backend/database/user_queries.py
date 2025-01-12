import aiomysql
from .db import get_connection, get_pool


async def insert_user(user_id: int, first_name: str, last_name: str, role: str):
    # SQL query to insert a new user into the 'users' table
    query = """
           INSERT INTO users (user_id, first_name, last_name, role) 
           VALUES (%s, %s, %s, %s)
       """
    connection = None
    try:
        # connect to the database
        connection = await get_connection()
        async with connection.cursor() as cursor:
            # execute the sql query with the given parameters using cursor
            await cursor.execute(query, (user_id, first_name, last_name, role))
            # # Commit changes to the database
            # await connection.commit()
            print("User added successfully.\n")
    except Exception as e:
        print(f"Error while inserting user: {e}")

    finally:
        # Zwolnij połączenie do puli, jeżeli zostało pobrane
        if connection:
            pool = await get_pool()
            await pool.release(connection)  # Możesz użyć await pool.release(connection) zamiast get_pool()
            print("Connection released back to the pool.")


async def update_user_role(user_id: int, role: str):
    query = "UPDATE users SET role = %s WHERE user_id = %s"
    try:
        async with get_connection() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(query, (role, user_id))
                print(f"User role was updated successfully:{role}\n")
    except Exception as e:
        print(f"Error while updating user role: {e}")


async def update_user_first_name(user_id: int, updated_first_name: str):
    query = "UPDATE users SET first_name = %s WHERE user_id = %s"
    try:
        async with get_connection() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(query, (updated_first_name, user_id))
                print(f"User first name was updated successfully:{updated_first_name}\n")
    except Exception as e:
        print(f"Error while updating user first name: {e}")


async def update_user_last_name(user_id: int, updated_last_name: str):
    query = "UPDATE users SET last_name = %s WHERE user_id = %s"
    try:
        async with get_connection() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(query, (updated_last_name, user_id))
                print(f"User last name was updated successfully:{updated_last_name}\n")
    except Exception as e:
        print(f"Error while updating user last name: {e}")


async def delete_user(user_id: int):
    query = "DELETE FROM users WHERE user_id = %s"
    try:
        async with get_connection() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(query, (user_id,))
                print(f"User with id({user_id}) deleted successfully.\n")
    except Exception as e:
        print(f"Error while deleting user: {e}")


async def select_user_by_id(user_id: int):
    query = "SELECT * FROM users WHERE user_id = %s"
    try:
        async with get_connection() as connection:
            async with connection.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, (user_id,))
                user_data = await cursor.fetchone()
                return user_data
    except Exception as e:
        print(f"Error while selecting user: {e}")
        return None
