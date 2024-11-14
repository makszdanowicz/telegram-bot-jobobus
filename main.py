import asyncio
import logging
from bot.bot import dp, bot


async def main():
    # Start polling - it means start listening for incoming messages and updated
    await dp.start_polling(bot)


# Bot execution entry point
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)  # Configure logging to display info-level logs in the console
    try:
        print('Bot is running')
        asyncio.run(main())  # Start the bot using asyncio
    except KeyboardInterrupt:
        # Handle shutdown of bot
        print('Bot is switch off')
