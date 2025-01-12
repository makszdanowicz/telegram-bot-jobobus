import asyncio
import logging
from bot.bot import dp, bot
from backend.database import create_pool, close_connection, get_connection


async def main():
    await create_pool()  # Initialize the database connection pool
    try:
        # Get the connection to the db
        await get_connection()

        # Start polling - it means start listening for incoming messages and updated
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        await close_connection()
    finally:
        # Ensure connection closure if the bot stops normally
        await close_connection()


# Bot execution entry point
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)  # Configure logging to display info-level logs in the console
    try:
        print('Bot is running')
        asyncio.run(main())  # Start the bot using asyncio
    except KeyboardInterrupt:
        # Handle shutdown of bot
        print('Bot is switch off')
