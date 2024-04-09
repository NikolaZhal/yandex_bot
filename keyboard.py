from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove


async def close_keyboarder(update, context):
    await update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardRemove()
    )
async def home_keyboarder(update, context):
    await update.message.reply_html(
        rf"to home",
        reply_markup=base_markup
    )
async def dice_keyboarder(update, context):
    await update.message.reply_html(
        rf"to cube",
        reply_markup=dice_markup
    )
async def time_keyboarder(update, context):
    await update.message.reply_html(
        rf"to timers",
        reply_markup=time_markup
    )


reply_keyboard = [['/dice', '/timer']]
base_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

dice_keyboard = [['/cube', '/cube 2'], ['/cube 1 20', '/home']]
dice_markup = ReplyKeyboardMarkup(dice_keyboard, one_time_keyboard=False)

time_keyboard = [['/timer_set 30', '/timer_set 60'], ['/timer_set 300', '/home']]
time_markup = ReplyKeyboardMarkup(time_keyboard, one_time_keyboard=False)

time_close_keyboard = [['/close']]
time_close_markup = ReplyKeyboardMarkup(time_close_keyboard, one_time_keyboard=False)
