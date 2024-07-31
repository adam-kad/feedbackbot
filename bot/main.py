import argparse
import logging

from bot import settings
from bot.handlers import default
from bot.settings import bot


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def run_handlers():
    bot.register_message_handler(default.start_handler, commands=["start"])
    bot.register_message_handler(default.help_handler, commands=["help"])
    bot.register_message_handler(default.info_handler, commands=["info"])

    parser = argparse.ArgumentParser(description="Telegram bot settings")
    parser.add_argument('--webhook', action='store_true', help='Enable webhook mode')
    args = parser.parse_args()

    if args.webhook:
        settings.setup_webhook()
    else:
        settings.run_polling()


if __name__ == '__main__':
    run_handlers()
