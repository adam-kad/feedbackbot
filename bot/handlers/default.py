from bot import constants
from bot.settings import bot


def start_handler(message):
    try:
        bot.send_message(message.chat.id, constants.START_MESSAGE, disable_web_page_preview=True)
    except Exception as err:
        print(err.args)


def help_handler(message):
    try:
        bot.send_message(message.chat.id, constants.HELP_MESSAGE, disable_web_page_preview=True)
    except Exception as err:
        print(err.args)


def info_handler(message):
    try:
        bot.send_message(message.chat.id, constants.INFO_MESSAGE, disable_web_page_preview=True)
    except Exception as err:
        print(err.args)
