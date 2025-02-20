import logging
from aiogram import Bot, Dispatcher

import os
from dotenv import load_dotenv

from bot.handlers.start.start_handlers import start_router
from bot.handlers.employee.employee_handlers import employee_router
from bot.handlers.employee.application_handlers import application_router
from bot.handlers.employee.job_search_handlers import searching_job_router
from bot.handlers.employer.employer_handlers import employer_router
from bot.handlers.employer.job_offers_handlers import job_offers_router
from bot.handlers.employer.candidates_handlers import candidates_router

# Reading API token for bot from .env config file
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

# Bot initialization
bot = Bot(token=API_TOKEN)

# Initialize the dispatcher to handle bot updates and routing
dp = Dispatcher()
# Registrate the routers with the dispatcher (handlers for different commands and messages)
dp.include_router(start_router)
dp.include_router(employee_router)
dp.include_router(application_router)
dp.include_router(searching_job_router)
dp.include_router(employer_router)
dp.include_router(job_offers_router)
dp.include_router(candidates_router)
