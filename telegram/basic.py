from connection import supabaseinteraction as supa
from connection.exceptions import UserNotRegisteredError
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    InvalidCallbackData,
)
from cogs import private_check
import uuid
import sys

sys.path.append('.')


async def start_private(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    name = update.message.from_user.full_name
    await update.message.reply_text("Hi! Welcome to your trusty personal assistant and scheduler, Ka.Y.E!"
                                    "\n Use /createevent to create a new event, or check out the bot menu to explore "
                                    "all my functionalities!")
    try:
        id = await supa.get_user_uuid(TeleID=user_id)
        await supa.signup({
            "id": id,
            "TeleID": user_id,
            "username": name
        })
    except UserNotRegisteredError as e:
        await supa.signup({
            "id": str(uuid.uuid4()),
            "TeleID": user_id,
            "username": name,
            "created_externally": True
        })


async def start_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    name = update.message.from_user.full_name
    await update.message.reply_text("Hi! Welcome to your trusty personal assistant and scheduler, Ka.Y.E!"
                                    "\n Head over to my DMs and use /createevent to create a new event, "
                                    "or check out the bot menu to explore "
                                    "all my functionalities!")
    id = await supa.get_user_uuid(TeleID=user_id)
    await supa.signup({
        "id": id if id else str(uuid.uuid4()),
        "TeleID": user_id,
        "username": name
    })


def start():
    return CommandHandler("start", private_check(start_private, start_group))


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    await update.message.reply_text(
        "Welcome back to your trusty personal assistant and scheduler, Ka.Y.E!"
        "Use /createevent in a DM with me to create an event, and send out your rsvp with /send_rsvp in your group!"
        "Feel free to explore my menu to see all of my functionalities and their description :)"
    )


def help():
    return CommandHandler("help", help_command)


async def handle_invalid_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Informs the user that the button is no longer available."""
    await update.callback_query.answer()
    await update.effective_message.edit_text(
        "Sorry, I could not process this button click 😕"
    )

