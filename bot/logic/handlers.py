from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot import constants
from bot.settings import bot, TELEGRAM_GROUP_ID


def start_handler(message):
    bot.send_message(message.chat.id, constants.START_MESSAGE, disable_web_page_preview=True)


def help_handler(message):
    bot.send_message(message.chat.id, constants.HELP_MESSAGE, disable_web_page_preview=True)


def info_handler(message):
    bot.send_message(message.chat.id, constants.INFO_MESSAGE, disable_web_page_preview=True)


def group_id_handler(message):
    if message.chat.type in ["group", "supergroup"]:
        bot.send_message(message.chat.id, f"Group ID: {message.chat.id}")
    else:
        bot.send_message(message.chat.id, "This chat is not a group chat")


def forward_message_to_admin(message):
    tg_chat_id = message.chat.id

    inline_markup = InlineKeyboardMarkup(row_width=2)
    next_exercise_button = [
        InlineKeyboardButton(
            text="Answer",
            callback_data=f"answer_id_{tg_chat_id}_{message.message_id}",
        ),
        InlineKeyboardButton(
            text="Delete",
            callback_data=f"remove_id",
        ),
        InlineKeyboardButton(
            text="🚫 Add to blacklist", callback_data=f"blacklist_add_{tg_chat_id}"
        ),
    ]
    inline_markup.add(*next_exercise_button)

    bot.send_message(
        TELEGRAM_GROUP_ID,
        f"💌: @{message.chat.username}"
        f"\n\n{message.text}",
        reply_markup=inline_markup,
    )

    bot.reply_to(message, "Your message has been sent")


def send_answer_handler(message):
    reply_to_message = message.reply_to_message.text
    user_tg_chat_id = reply_to_message.split(" ")[0][1:-1]
    user_message_id = reply_to_message.split(" ")[1][1:-1]

    try:
        bot.send_message(
            user_tg_chat_id,
            message.text,
            reply_to_message_id=user_message_id,
        )
    except AttributeError:
        bot.send_message(
            user_tg_chat_id,
            message.text,
        )
    bot.send_message(
        message.chat.id, f"Сообщение для @ успешно отправлено!"
    )
