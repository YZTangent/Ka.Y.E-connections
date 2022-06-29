from connection import supabaseinteraction as supa
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    InvalidCallbackData,
)
from cogs import private_check
import sys

sys.path.append('.')


async def start_private(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    name = update.message.from_user.full_name
    await supa.signup({
        "TeleID": user_id,
        "username": name
    })
    await update.message.reply_text("Hi! Welcome back to your trusty personal assistant and scheduler, Ka.Y.E!"
                                    "Press start ")


async def start_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    return


def start():
    return CommandHandler("start", private_check(start_private, start_group))


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    await update.message.reply_text(
        "Use /start to test this bot. Use /clear to clear the stored data so that you can see "
        "what happens, if the button data is not available. "
    )


async def handle_invalid_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Informs the user that the button is no longer available."""
    await update.callback_query.answer()
    await update.effective_message.edit_text(
        "Sorry, I could not process this button click 😕"
    )

