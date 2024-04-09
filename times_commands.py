from datetime import datetime
from keyboard import base_markup, time_markup, time_close_markup, dice_keyboarder, time_keyboarder
async def time_command(update, context):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text(
        f"Часы: {datetime.now().hour} \nминуты: {datetime.now().minute}\nсекуды: {datetime.now().second}")


async def data_command(update, context):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text(f"{datetime.now().date()}")


TIMER = 5  # таймер на 5 секунд


def remove_job_if_exists(name, context):
    """Удаляем задачу по имени.
    Возвращаем True если задача была успешно удалена."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


# Обычный обработчик, как и те, которыми мы пользовались раньше.
async def set_timer(update, context):
    """Добавляем задачу в очередь"""
    chat_id = update.effective_message.chat_id
    timer = int(context.args[0])
    # Добавляем задачу в очередь
    # и останавливаем предыдущую (если она была)
    job_removed = remove_job_if_exists(str(chat_id), context)
    context.job_queue.run_once(task, timer, chat_id=chat_id, name=str(chat_id), data=timer)

    text = f'Вернусь через {timer} с.!'
    if job_removed:
        text += ' Старая задача удалена.'
    await update.effective_message.reply_text(text, reply_markup=time_close_markup)


async def task(context):
    """Выводит сообщение"""
    await context.bot.send_message(context.job.chat_id, text=f'КУКУ! {context.job.data} c. прошли!', reply_markup=time_markup)


async def unset(update, context):
    """Удаляет задачу, если пользователь передумал"""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Таймер отменен!' if job_removed else 'У вас нет активных таймеров'
    await update.message.reply_text(text, reply_markup=time_markup)
