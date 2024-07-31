import http.server
import socketserver
import json
import logging

from telebot import TeleBot, types
from . import config


TELEGRAM_BOT_TOKEN = config.telegram_bot_token.get_secret_value()
TELEGRAM_WEBHOOK_URL = config.telegram_webhook_url
TELEGRAM_WEBHOOK_PORT = config.telegram_webhook_port

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

bot = TeleBot(TELEGRAM_BOT_TOKEN, parse_mode="HTML")


def is_webhook_set():
    webhook_info = bot.get_webhook_info()
    if webhook_info.url == TELEGRAM_WEBHOOK_URL:
        logger.info("Webhook is already set.")
        return True
    return False


def setup_webhook():
    try:
        if not is_webhook_set():
            bot.remove_webhook()
            response = bot.set_webhook(url=TELEGRAM_WEBHOOK_URL)
            if response:
                logger.info("Webhook set successfully")
                run_webhook_server()
            else:
                logger.error("Failed to set webhook")
        else:
            run_webhook_server()
    except Exception as e:
        logger.error(f"Error setting webhook: {e}")


def run_webhook_server(port=TELEGRAM_WEBHOOK_PORT):
    class RequestHandler(http.server.SimpleHTTPRequestHandler):
        def do_POST(self):
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                update = json.loads(post_data.decode('utf-8'))

                bot.process_new_updates([types.Update.de_json(update)])
                self.send_response(200)
            except Exception as e:
                logger.error(f"Error processing request: {e}")
                self.send_response(500)
            finally:
                self.end_headers()

    with socketserver.TCPServer(("", port), RequestHandler) as httpd:
        logger.info(f"Serving at port {port} for webhook")
        httpd.serve_forever()


def run_polling():
    if is_webhook_set():
        bot.remove_webhook()

    logger.info("Running in polling mode")
    bot.polling(none_stop=True)
