import json
import logging
from aiogram import Bot, Dispatcher

from bot.handlers.start.start_handlers import start_router
from bot.handlers.employee.employee_handlers import employee_router


# function that load and read api token from config json file
def load_api_token(config_path=r'bot/config/bot_config.json'):
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
            print(config.get('API_TOKEN'))
        return config.get('API_TOKEN')  # Returning only token
    except Exception as e:
        logging.error(f"Failed to load config file {config_path}: {e}")
        return None


API_TOKEN = load_api_token()

# Bot initialization
bot = Bot(token=API_TOKEN)

# Initialize the dispatcher to handle bot updates and routing
dp = Dispatcher()
# Registrate the routers with the dispatcher (handlers for different commands and messages)
dp.include_router(start_router)
dp.include_router(employee_router)
