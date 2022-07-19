from connection import supabaseinteraction as supa
from connection.exceptions import UserNotRegisteredError, InvalidDatetimeError
from connection.helper import past_future_check, datetime_validation
from datetime import datetime
from telegram import Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
)
from cogs import private_check
import uuid


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
            "guest_user": True
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


async def get_id_handler(update, context):
    await update.message.reply_text(update.message.from_user.id)


def get_id():
    return CommandHandler("get_id", get_id_handler)


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


async def set_birthday_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    try:
        bday = context.args[0].replace("/", "-")
        year, month, day = bday.split("-")
        if past_future_check(datetime_validation(int(year), int(month), int(day))) != "past":
            await update.message.reply_text(
                "Invalid Date!"
            )
            return
    except IndexError:
        await update.message.reply_text(
            "Please provide a date!"
        )
    except InvalidDatetimeError:
        await update.message.reply_text(
            "Invalid Date!"
        )
    try:
        id = await supa.get_user_uuid(TeleID=user_id)
        await update.message.reply_text(
            "Your birthday has been updated!"
        )
        await supa.update_birthday({
            'id': id,
            'bday': bday
        })
    except UserNotRegisteredError as e:
        await update.effective_user.send_message(
            "Please register with the bot first with /start!"
        )


def set_birthday():
    return CommandHandler("set_birthday", set_birthday_command)