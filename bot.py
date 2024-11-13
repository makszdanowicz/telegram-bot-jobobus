import logging
import json
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command

from handlers import router


# API_TOKEN = '7713099196:AAE4_6_w0Z6WZ401bWH40xjLWIBkZAEGaIs'
# function that read api token from config json file
def load_api_token(config_path='bot/bot_config.json'):
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config.get('API_TOKEN')  # Returning only token
    except Exception as e:
        logging.error(f"Failed to load config file {config_path}: {e}")
        return None


API_TOKEN = load_api_token()

# Bot initialization
bot = Bot(token=API_TOKEN)

# Dispatcher initialization
dp = Dispatcher()
dp.include_router(router)
