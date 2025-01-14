import aiomysql
from backend.database import get_connection, get_pool, execute_query


async def insert_employer(user_id: int, company_name: str):
    query = """
            INSERT INTO employers (user_id, company_name)
            VALUES (%s, %s)
        """
    await execute_query(query, (user_id, company_name), fetch_type="none")
    # connection = None
    # try:
    #     connection = await get_connection()
    #     async with connection.cursor() as cursor:
    #         await cursor.execute(query, (user_id, company_name))
    #         print("Employer added successfully.\n")
    # except Exception as e:
    #     print(f"Error while inserting employer: {e}")
    # finally:
    #     if connection:
    #         pool = await get_pool()
    #         await pool.release(connection)
    #         print("Connection released back to the pool.")


async def change_employer_company_name(user_id: int, updated_company_name: str):
    query = "UPDATE employers SET company_name = %s WHERE user_id = %s"
    await execute_query(query, (updated_company_name, user_id), fetch_type="none")
    # connection = None
    # try:
    #     connection = await get_connection()
    #     async with connection.cursor() as cursor:
    #         await cursor.execute(query, (updated_company_name, user_id))
    #         print(f"Employer company name updated successfully: {updated_company_name}\n")
    # except Exception as e:
    #     print(f"Error while updating employer company name: {e}")
    # finally:
    #     if connection:
    #         pool = await get_pool()
    #         await pool.release(connection)
    #         print("Connection released back to the pool.")


async def select_employer_by_id(user_id: int):
    query = """
            SELECT u.first_name, u.last_name, u.role, e.company_name
            FROM users u
            INNER JOIN employers e ON u.user_id = e.user_id
            WHERE u.user_id = %s
        """
    await execute_query(query, (user_id,), fetch_type="one")
    # connection = None
    # try:
    #     connection = await get_connection()
    #     async with connection.cursor(aiomysql.DictCursor) as cursor:
    #         await cursor.execute(query, (user_id,))
    #         employer_data = await cursor.fetchone()
    #         return employer_data
    # except Exception as e:
    #     print(f"Error while selecting employer: {e}")
    #     return None
    # finally:
    #     if connection:
    #         pool = await get_pool()
    #         await pool.release(connection)
    #         print("Connection released back to the pool.")


async def delete_employer(user_id: int):
    query = "DELETE FROM employers WHERE user_id = %s"
    await execute_query(query, (user_id,), fetch_type="none")
    # connection = None
    # try:
    #     connection = await get_connection()
    #     async with connection.cursor() as cursor:
    #         await cursor.execute(query, (user_id,))
    #         print(f"Employer with id({user_id}) deleted successfully.\n")
    # except Exception as e:
    #     print(f"Error while deleting employer: {e}")
    # finally:
    #     if connection:
    #         pool = await get_pool()
    #         await pool.release(connection)
    #         print("Connection released back to the pool.")
