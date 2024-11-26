import aiomysql
import json


async def create_connection():
    # Reading database configuration data from a JSON file
    with open('backend/bot_config.json', 'r') as config_file:
        config_data = json.load(config_file)

    # Creating database connection
    connection = await aiomysql.connect(
        host=config_data["host"],
        user=config_data["user"],
        password=config_data["password"],
        db=config_data["database"]
    )

    return connection