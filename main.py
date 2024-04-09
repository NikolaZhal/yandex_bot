import logging
from random import randint

from telegram.ext import Application, MessageHandler, filters
from telegram.ext import CommandHandler

from config import BOT_TOKEN
from keyboard import base_markup, close_keyboarder, home_keyboarder, dice_keyboarder, time_keyboarder
from times_commands import time_command, data_command, set_timer, unset

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


async def echo(update, context):
    await update.message.reply_text(f'Я получил сообщение {update.message.text}')


async def start(update, context):
    """Отправляет сообщение когда получена команда /start"""
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я эхо-бот. Напишите мне что-нибудь, и я пришлю это назад!",
        reply_markup=base_markup
    )


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

    application.add_handler(CommandHandler("start", start))
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

    # Регистрируем обработчик в приложении.
    application.add_handler(text_handler)

    # Запускаем приложение.
    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
