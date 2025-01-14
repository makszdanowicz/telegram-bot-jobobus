from typing import Optional

import aiomysql
import os
from dotenv import load_dotenv

# Load environment variables from .env config file using specified path
load_dotenv(dotenv_path="backend/database/db_config.env")

# Read database configuration data from environment variables
db_config_data = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT")),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

# Declaration of pool of connections to the db
pool: Optional[aiomysql.Pool] = None


# Function to create and initialize the connection pool
async def create_pool():
    global pool

    # Create a connection pool with specified parameters from config
    pool = await aiomysql.create_pool(
        host=db_config_data["host"],
        user=db_config_data["user"],
        password=db_config_data["password"],
        db=db_config_data["database"],
        minsize=1,
        maxsize=10,
        autocommit=True
    )


# Function to get a connection from the pool
async def get_connection():
    global pool
    if pool is None:
        raise Exception("Pool is not initialized. Call create_pool() first.")
    connection = await pool.acquire()  # await the coroutine to get the connection
    print("Connection is initialized!")
    return connection


async def get_pool():
    global pool
    if pool is None:
        raise Exception("Pool is not initialized. Call create_pool() first.")
    return pool


# Function to close the connection pool
async def close_connection():
    global pool
    if pool:
        # Close the pool and wait for all connections to be properly closed
        pool.close()
        await pool.wait_closed()  # closing all open connections
    else:
        print("Pool was not initialized or already closed.")


# Executes an SQL query and returns results based on the fetch_type.
async def execute_query(query: str, arguments: tuple = (), fetch_type: str = "none"):
    connection = None
    try:
        connection = await get_connection()
        async with connection.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute(query, arguments)
            if fetch_type == "none":
                # For INSERT, UPDATE, DELETE, no data is returned
                return None
            elif fetch_type == "one":
                # For SELECT queries expecting a single record
                return await cursor.fetchone()
            elif fetch_type == "all":
                # For SELECT queries expecting multiple records
                return await cursor.fetchall()
            else:
                raise ValueError(f"Unknown fetch_type: {fetch_type}")
    except Exception as e:
        print(f"Error while executing query: {e}")
        return None
    finally:
        if connection:
            global pool
            await pool.release(connection)
            print("Connection released back to the pool.")
