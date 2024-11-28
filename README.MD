## How to Run

1. **Clone the repository:**

    ```sh
    git clone https://github.com/makszdanowicz/telegram-bot-jobobus
    cd telegram-bot-jobobus
    ```

2. **Create config file and add API token:**

    ```sh
    echo '{"API_TOKEN": "your-telegram-bot-token"}' > bot/bot_config.json
    ```
    
3. **Set up and activate environment:**
    Create a `.venv` file in the root directory and add your Telegram bot token:

    ```sh
    python -m venv .venv
    .\.venv\Scripts\activate
    ```
4. **Install dependencies into your environment:**

    ```sh
    pip install -r requirements.txt
    ```

5. **Run the bot:**

    ```sh
    python bot.py
    ```

6. **Interact with your bot on Telegram.**

https://t.me/JobOBusBot
