import argparse
import logging

from bot import settings
from bot.logic import handlers, callbacks
from bot.settings import bot


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def run_handlers():
    bot.register_message_handler(handlers.start_handler, commands=["start"])
    bot.register_message_handler(handlers.help_handler, commands=["help"])
    bot.register_message_handler(handlers.info_handler, commands=["info"])
    bot.register_message_handler(handlers.group_id_handler, commands=["send_group_id"])
    bot.register_message_handler(
        handlers.forward_message_to_admin,
        func=lambda message: message.chat.type == 'private' and not message.text.startswith('/')
    )
    bot.register_message_handler(
        handlers.send_answer_handler,
        func=lambda message: message.reply_to_message
        and message.reply_to_message.text.startswith('[')
        and 'Введите ответ на сообщение' in message.reply_to_message.text
    )

    bot.register_callback_query_handler(
        callbacks.remove_feedback_callback,
        func=lambda call: call.data.startswith('remove_id'),
    )
    bot.register_callback_query_handler(
        callbacks.answer_feedback_callback,
        func=lambda call: call.data.startswith('answer_id'),
    )

    parser = argparse.ArgumentParser(description="Telegram bot settings")
    parser.add_argument('--webhook', action='store_true', help='Enable webhook mode')
    args = parser.parse_args()

    if args.webhook:
        settings.setup_webhook()
    else:
        settings.run_polling()


if __name__ == '__main__':
    run_handlers()
