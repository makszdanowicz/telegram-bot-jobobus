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
    async with pool.acquire() as connection:
        print("Connection is initialized!")
        return connection


# Function to close the connection pool
async def close_connection():
    global pool
    if pool:
        # Close the pool and wait for all connections to be properly closed
        pool.close()
        await pool.wait_closed()
    else:
        print("Pool was not initialized or already closed.")
