# Feedback Bot

Feedback Bot is a Telegram bot designed to provide feedback and assistance. This bot is built using Python and the `pytelegrambotapi` library. You are welcome to contribute and help improve this bot. Visit our [GitHub page](https://github.com/adam-kad/feedbackbot) for more details.

## Requirements

- Python 3.11+
- Poetry for dependency management
- `pytelegrambotapi` library

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/adam-kad/feedbackbot.git
    cd feedbackbot
    ```

2. **Install Poetry:**

    Follow the instructions on the [Poetry installation page](https://python-poetry.org/docs/#installation).

3. **Install dependencies:**

    ```sh
    poetry install
    ```

## Configuration

1. **Set up your Telegram bot:**

    - Create a new bot using [BotFather](https://core.telegram.org/bots#botfather) and obtain your bot token.
    - Create a file named `.env` in the `feedbackbot/config` directory and add your bot token and other configuration settings:

        ```env
        TELEGRAM_BOT_TOKEN=your_bot_token_here
        TELEGRAM_WEBHOOK_URL=https://your-webhook-url-here
        PORT=8000
        ```

2. **Configure webhook (optional):**

    - If you are developing locally and want to use webhooks, you need to expose your local server to the internet. You can use [ngrok](https://ngrok.com/) for this purpose. Download and install ngrok, then run:

      ```sh
      ngrok http 8000
      ```

    - Use the generated ngrok URL as your `TELEGRAM_WEBHOOK_URL` and `TELEGRAM_WEBHOOK_PORT` in the `.env` file.

## Usage

1. **Run the bot in polling mode:**

    ```sh
    poetry run python -m bot.main
    ```

2. **Run the bot in webhook mode:**

    ```sh
    poetry run python -m bot.main --webhook
    ```

## Contributing

We invite you to contribute and help make this bot better.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

Best regards, Feedback Bot
