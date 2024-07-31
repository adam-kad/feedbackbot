from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot import constants, utils
from bot.settings import bot, TELEGRAM_GROUP_ID


def check_admin_status(func):
    def wrapper(message):
        chat_member = bot.get_chat_member(TELEGRAM_GROUP_ID, message.from_user.id)
        if chat_member.status in ['administrator', 'creator']:
            return func(message)

    return wrapper


def check_blacklist(func):
    def wrapper(message):
        blacklist = utils.read_blacklist()
        if str(message.from_user.id) in blacklist:
            bot.send_message(
                message.chat.id,
                "You are on the blacklist."
            )
        else:
            return func(message)
    return wrapper


@check_blacklist
def start_handler(message):
    bot.send_message(message.chat.id, constants.START_MESSAGE, disable_web_page_preview=True)


@check_blacklist
def help_handler(message):
    bot.send_message(message.chat.id, constants.HELP_MESSAGE, disable_web_page_preview=True)


@check_blacklist
def info_handler(message):
    bot.send_message(message.chat.id, constants.INFO_MESSAGE, disable_web_page_preview=True)


@check_admin_status
def forgive_handler(message):
    try:
        user_id = message.text.split()[1]
        blacklist = utils.read_blacklist()
        if user_id in blacklist:
            utils.remove_from_blacklist(user_id)
            bot.send_message(message.chat.id, f"User {user_id} is excluded from the third list.")
        else:
            bot.send_message(message.chat.id, "The user is not blacklisted.")
    except IndexError:
        bot.send_message(
            message.chat.id,
            "Specify the user ID to exclude from the blacklist. For example: /forgive 111"
        )


@check_blacklist
def group_id_handler(message):
    if message.chat.type in ["group", "supergroup"]:
        bot.send_message(message.chat.id, f"Group ID: {message.chat.id}")
    else:
        bot.send_message(message.chat.id, "This chat is not a group chat")


@check_blacklist
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
        message.chat.id, f"Message for <b>ID:{user_tg_chat_id}</b> successfully sent!"
    )
