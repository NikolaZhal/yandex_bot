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

stih = """Идет бычок, качается,
Вздыхает на ходу:
— Ох, доска кончается,
Сейчас я упаду!""".split('\n')


async def starter(update, context):
    context.user_data['string'] = 1
    await update.message.reply_text(stih[0])
    return 1


# Добавили словарь user_data в параметры.
async def next_string_response(update, context):
    # Сохраняем ответ в словаре.
    if stih[context.user_data['string']] == update.message.text:
        await update.message.reply_text(f"{stih[context.user_data['string'] + 1]}")
        context.user_data['string'] += 2
    else:
        await update.message.reply_text(f'''нет, не так''')
        await update.message.reply_text(stih[context.user_data['string']])

    return 1


async def suphler_command(update, context):
    await update.message.reply_text(stih[context.user_data['string']])
    return 1


async def stop(update, context):
    await update.message.reply_text("Всего доброго!")
    return ConversationHandler.END


stih_handler = ConversationHandler(
    # Точка входа в диалог.
    # В данном случае — команда /start. Она задаёт первый вопрос.
    entry_points=[CommandHandler('start', starter)],

    # Состояние внутри диалога.
    # Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
    states={
        # Функция читает ответ на первый вопрос и задаёт второй.
        1: [MessageHandler(filters.TEXT & ~filters.COMMAND, next_string_response),
            CommandHandler("suphler", suphler_command)]
    },

    # Точка прерывания диалога. В данном случае — команда /stop.
    fallbacks=[CommandHandler('stop', stop)]
)


async def echo(update, context):
    await update.message.reply_text(f'Я получил сообщение {update.message.text}')


async def help_command(update, context):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text("/entry - вход в музей")


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

    # Регистрируем обработчик в приложении.
    application.add_handler(stih_handler)

    # Запускаем приложение.
    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
