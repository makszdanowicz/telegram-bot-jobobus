import asyncio
import logging
from bot.bot import dp, bot
from backend.database import create_pool, close_connection, get_connection


# Function to gracefully shut down resources
async def shutdown():
    logging.info("Shutting down...")
    await close_connection()  # Close the database connection pool
    logging.info("Shutdown completed.")


async def main():
    await create_pool()  # Initialize the database connection pool
    try:
        # Start polling - it means start listening for incoming messages and updated
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        # Ensure connection closure if the bot stops
        await shutdown()  # Perform shutdown before exit


# Bot execution entry point
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)  # Configure logging to display info-level logs in the console
    try:
        print('Bot is running')
        asyncio.run(main())  # Start the bot using asyncio
    except KeyboardInterrupt:
        # Handle shutdown of bot
        print('Bot is switching off')
    finally:
        # Make sure the event loop is closed properly
        logging.info("Bot execution finished.")
