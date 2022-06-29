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


async def build_rsvp_message(event_info) -> InlineKeyboardMarkup:
    coming = await supa.get_rsvp_by_event(event_info['id'], True)
    not_coming = await supa.get_rsvp_by_event(event_info['id'], False)
    text = "please rsvp to event {}" \
           "\nLocation: {}" \
           "\nComing: {}" \
           "\nNot Coming:{}"\
        .format(event_info['activity'],
<<<<<<< HEAD
                "\n" + event_info['description'] + "\n" if event_info['description'] else "",
                "\n" + "*Date:*" + event_info['starttime'][0:10].replace("-", "\/") + "\n" + "\n*Time:* "
                + event_info['starttime'][11:].replace("-", " UTC\-").replace("+", " UTC\+")
                    if event_info['starttime'] else "\n*Time:* TBC",
                event_info['location'] if event_info['location'] else "TBC")
=======
                event_info['location'] if event_info['location'] else "TBC",
                str(coming),
                str(not_coming))
>>>>>>> 395d8cb2c3c1400898f22bd9a3cab29557095b85

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Yes, I'm coming!", callback_data=("rsvp", True, event_info))],
        [InlineKeyboardButton("No, I can't make it :(", callback_data=("rsvp", False, event_info))],
    ])
    return text, keyboard


async def send_rsvp_private(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Hi! Please send your RSVP to a group."
    )


async def send_rsvp_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    # events = supa.get_user_event(user_id)
    events = await supa.get_all_events()
    keyboard = InlineKeyboardMarkup.from_column(
        [InlineKeyboardButton(i['activity'], callback_data=("events", i, user_id)) for i in events]
    )
    text = "Please select your event!"
    await update.message.reply_text(text, reply_markup=keyboard)


async def load_rsvp_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    update.callback_query.
    _, event_info, user_id = query.data
    # if query.from_user.id == user_id:
    await query.answer()
    # Get the data from the callback_data.
    # append the number to the list

    text, keyboard = await build_rsvp_message(event_info)
    await query.edit_message_text(
        text=text,
        reply_markup=keyboard,
    )
    # else:
    #     await query.answer()
    #     await context.bot.sendMessage()

    # we can delete the data stored for the query, because we've replaced the buttons
    context.drop_callback_data(query)


async def handle_rsvp_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    _, available, event_info = query.data
    user_id = await supa.get_user_uuid(TeleID=query.from_user.id)
    rsvp_info = {
        "userID": user_id,
        "eventID": event_info['id'],
        "avail": available,
    }
    await query.answer()
    await supa.set_rsvp(rsvp_info)
    text, keyboard = await build_rsvp_message(event_info)
    await query.edit_message_text(
        text=text,
        reply_markup=keyboard,
    )


def choose_rsvp():
    return CommandHandler("send_rsvp", private_check(send_rsvp_private, send_rsvp_group))


def send_rsvp():
    return CallbackQueryHandler(load_rsvp_message, lambda callback: callback[0] == "events")


def handle_rsvp():
    return CallbackQueryHandler(handle_rsvp_message, lambda callback: callback[0] == "rsvp")