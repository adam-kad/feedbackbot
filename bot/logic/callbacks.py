from bot import utils
from bot.settings import bot, TELEGRAM_GROUP_ID


def check_admin_status(func):
    def wrapper(call):
        chat_member = bot.get_chat_member(TELEGRAM_GROUP_ID, call.from_user.id)
        if chat_member.status in ['administrator', 'creator']:
            return func(call)

    return wrapper


@check_admin_status
def remove_feedback_callback(call):
    username = call.message.text.split("\n")[0][4:]

    bot.delete_message(TELEGRAM_GROUP_ID, call.message.message_id)
    bot.send_message(
        TELEGRAM_GROUP_ID,
        f"<b>Message from @{username} successfully deleted!</b>",
    )


@check_admin_status
def answer_feedback_callback(call):
    data = call.data.split("_")

    user_chat_id = data[2]
    user_message_id = data[3]

    bot.send_message(
        call.message.chat.id,
        f"[{user_chat_id}] [{user_message_id}] "
        f"\n\nEnter a reply to the message Reply to this message:",
    )


@check_admin_status
def blacklist_feedback_callback(call):
    data = call.data.split("_")
    user_chat_id = data[2]
    username = call.message.text.split("\n")[0][4:]

    utils.add_to_blacklist(user_chat_id)

    bot.delete_message(TELEGRAM_GROUP_ID, call.message.message_id)
    bot.send_message(
        TELEGRAM_GROUP_ID,
        f"User @{username} has been added to the blacklist!"
        f"To remove a user from the blacklist, use /forgive",
    )
