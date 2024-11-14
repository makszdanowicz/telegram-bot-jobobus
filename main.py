import asyncio
import logging
from bot.bot import dp, bot  # Importujemy dispatcher  i bot z pliku `bot.py`


async def main():
    # Rozpoczynamy polling, czyli nasłuchiwanie nowych wiadomości
    await dp.start_polling(bot)

# Uruchomienie bota
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO) # getting logs to console about all interactions with bot
    try:
        print('Bot is running')
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot is switch off')