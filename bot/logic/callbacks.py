from bot.settings import bot, TELEGRAM_GROUP_ID


def check_admin_status(func):
    def wrapper(call):
        chat_member = bot.get_chat_member(TELEGRAM_GROUP_ID, call.from_user.id)
        if chat_member.status in ['administrator', 'creator']:
            return func(call)

    return wrapper


def remove_feedback_callback(call):
    username = call.message.text.split("\n")[0][4:]

    bot.delete_message(TELEGRAM_GROUP_ID, call.message.message_id)
    bot.send_message(
        TELEGRAM_GROUP_ID,
        f"<b>Сообщение от @{username} успешно удалено!</b>",
    )


@check_admin_status
def answer_feedback_callback(call):
    data = call.data.split("_")

    user_chat_id = data[2]
    user_message_id = data[3]

    bot.send_message(
        call.message.chat.id,
        f"[{user_chat_id}] [{user_message_id}] "
        f"\n\nВведите ответ на сообщение реплаем на это сообщение:",
    )

