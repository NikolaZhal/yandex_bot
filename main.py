import logging
from random import randint

from telegram.ext import Application, MessageHandler, filters
from telegram.ext import CommandHandler, ConversationHandler

from config import BOT_TOKEN
from keyboard import close_keyboarder, home_keyboarder, dice_keyboarder, time_keyboarder
from times_commands import time_command, data_command, set_timer, unset

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


async def start(update, context):
    await update.message.reply_text(
        "Привет. Пройдите небольшой опрос, пожалуйста!\n"
        "Вы можете прервать опрос, послав команду /stop.\n"
        "В каком городе вы живёте?")

    # Число-ключ в словаре states —
    # втором параметре ConversationHandler'а.
    return 1
    # Оно указывает, что дальше на сообщения от этого пользователя
    # должен отвечать обработчик states[1].
    # До этого момента обработчиков текстовых сообщений
    # для этого пользователя не существовало,
    # поэтому текстовые сообщения игнорировались.


# Добавили словарь user_data в параметры.
async def first_response(update, context):
    # Сохраняем ответ в словаре.
    context.user_data['locality'] = update.message.text
    await update.message.reply_text(
        f"Какая погода в городе {context.user_data['locality']}?")
    return 2

async def skip_command(update, context):
    # Сохраняем ответ в словаре.
    context.user_data['locality'] = False
    await update.message.reply_text(
        f"Какая погода у вас за окном?")
    return 2


# Добавили словарь user_data в параметры.
async def second_response(update, context):
    weather = update.message.text
    logger.info(weather)
    # Используем user_data в ответе.
    if context.user_data['locality']:
        await update.message.reply_text(
            f"Спасибо за участие в опросе! Привет, {context.user_data['locality']}!")
    else:
        await update.message.reply_text(
            f"Спасибо за участие в опросе!")
    context.user_data.clear()  # очищаем словарь с пользовательскими данными
    return ConversationHandler.END


async def stop(update, context):
    await update.message.reply_text("Всего доброго!")
    return ConversationHandler.END


conv_handler = ConversationHandler(
    # Точка входа в диалог.
    # В данном случае — команда /start. Она задаёт первый вопрос.
    entry_points=[CommandHandler('start', start)],

    # Состояние внутри диалога.
    # Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
    states={
        # Функция читает ответ на первый вопрос и задаёт второй.
        1: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_response),
            CommandHandler("skip", skip_command)],
        # Функция читает ответ на второй вопрос и завершает диалог.
        2: [MessageHandler(filters.TEXT & ~filters.COMMAND, second_response)]
    },

    # Точка прерывания диалога. В данном случае — команда /stop.
    fallbacks=[CommandHandler('stop', stop)]
)


async def echo(update, context):
    await update.message.reply_text(f'Я получил сообщение {update.message.text}')


async def help_command(update, context):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text("Я пока не умею помогать... Я только ваше эхо.")


async def cube_command(update, context):
    chat_id = update.effective_message.chat_id
    cube_data = {'sides': 6, 'iters': 1}
    if len(context.args) == 2:
        cube_data['sides'] = int(context.args[1])
        cube_data['iters'] = int(context.args[0])
    elif len(context.args) == 1:
        cube_data['iters'] = int(context.args[0])
    text = f'Броски:\n'
    for i in range(cube_data['iters']):
        text += f"{i + 1}: {randint(0, cube_data['sides'])} \n"
    await update.effective_message.reply_text(text)


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    # app = ApplicationBuilder().token("TOKEN").proxy_url(proxy_url).build()

    text_handler = MessageHandler(filters.TEXT, echo)

    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("time", time_command))
    application.add_handler(CommandHandler("date", data_command))
    application.add_handler(CommandHandler("timer_set", set_timer))
    application.add_handler(CommandHandler("unset", unset))
    application.add_handler(CommandHandler("close", unset))
    application.add_handler(CommandHandler("home", home_keyboarder))
    application.add_handler(CommandHandler("dice", dice_keyboarder))
    application.add_handler(CommandHandler("timer", time_keyboarder))
    application.add_handler(CommandHandler("cube", cube_command))
    application.add_handler(CommandHandler("c", close_keyboarder))
    application.add_handler(CommandHandler("o", home_keyboarder))
    application.add_handler(conv_handler)

    # Регистрируем обработчик в приложении.
    application.add_handler(text_handler)

    # Запускаем приложение.
    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
