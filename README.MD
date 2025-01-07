![JobOBus Logo](logo.jpg)

## How to Run

1. **Clone the repository:**

    ```sh
    git clone https://github.com/makszdanowicz/telegram-bot-jobobus
    cd telegram-bot-jobobus
    ```

2. **Add API token to .env file:**

    Enter the API token to '.env.template' file and copy it into '.env'
    ```sh
    cp .env.template .env
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
    python main.py
    ```

6. **Interact with your bot on Telegram.**

https://t.me/JobOBusBot
