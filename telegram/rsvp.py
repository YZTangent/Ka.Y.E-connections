import sys
sys.path.append('.')
from connection import supabaseinteraction as supa
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Chat
from typing import List, Tuple, cast
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    InvalidCallbackData,
)
from cogs import private_check


async def build_event_list(user_id) -> InlineKeyboardMarkup:
    # events = supa.get_user_event(update['from']['id'])
    events = await supa.get_all_events()
    keyboard = InlineKeyboardMarkup.from_column(
        [InlineKeyboardButton(i['activity'], callback_data=("events", i)) for i in events]
    )
    text = "Please select your event!"
    return text, keyboard


def build_rsvp_message(event_info) -> InlineKeyboardMarkup:
    text = "please rsvp to event {}".format(event_info['activity'])

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Yes", callback_data=("rsvp", True, event_info))],
        [InlineKeyboardButton("No", callback_data=("rsvp", False, event_info))],
    ])
    return text, keyboard


async def send_rsvp_private(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Hi! Please send your RSVP to a group."
    )


async def send_rsvp_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        text, keyboard = await build_event_list(update.message.from_user.id)
        await update.message.reply_text(text, reply_markup=keyboard)


async def load_rsvp_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()
    # Get the data from the callback_data.
    _, event_info = query.data
    # append the number to the list

    text, keyboard = build_rsvp_message(event_info)

    await query.edit_message_text(
        text=text,
        reply_markup=keyboard,
    )

    # we can delete the data stored for the query, because we've replaced the buttons
    context.drop_callback_data(query)


def choose_rsvp():
    return CommandHandler("sendrsvp", private_check(send_rsvp_private, send_rsvp_group))


def send_rsvp():
    return CallbackQueryHandler(load_rsvp_message, lambda callback: callback[0] == "events")