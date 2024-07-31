from bot.settings import bot, TELEGRAM_GROUP_ID


def remove_feedback_callback(call):
    username = call.message.text.split("\n")[0][4:]

    bot.delete_message(TELEGRAM_GROUP_ID, call.message.message_id)
    bot.send_message(
        TELEGRAM_GROUP_ID,
        f"<b>Сообщение от @{username} успешно удалено!</b>",
    )
