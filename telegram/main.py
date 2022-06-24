import logging
import sys
sys.path.append('.')
from connection import supabaseinteraction as supa
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Chat
import asyncio
from typing import List, Tuple, cast
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    InvalidCallbackData,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


"""
-------------------------------------------- Private or Group checker --------------------------------------------------
"""
def privcheck(privatefunc, groupfunc):
    async def inner(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.chat.type == 'private':
            await privatefunc(update, context)
        else:
            await groupfunc(update, context)
    return inner


"""
-------------------------------------------- Element builders ----------------------------------------------------------
"""
def build_keyboard(current_list) -> InlineKeyboardMarkup:
    events = supa.get_event().data
    return InlineKeyboardMarkup.from_column(
        [InlineKeyboardButton(i['activity'], callback_data=("events", i)) for i in events]
    )


def build_event_list(update: Update) -> InlineKeyboardMarkup:
    # events = supa.get_user_event(update['from']['id']).data
    events = supa.get_all_events().data
    keyboard = InlineKeyboardMarkup.from_column(
        [InlineKeyboardButton(i['activity'], callback_data=("events", i)) for i in events]
    )
    text = "Please select your event!"
    return text, keyboard


def build_rsvp_message(update: Update) -> InlineKeyboardMarkup:
    events = supa.get_event().data
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Yes", callback_data=("rsvp", True))],
        [InlineKeyboardButton("No", callback_data=("events", False))],
    ])


"""
-------------------------------------------- Handlers ------------------------------------------------------------------
"""
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with 5 inline buttons attached."""
    print(update)
    if update.message.chat.type == 'private':
        await update.message.reply_text("cringe")
    else:
        text, keyboard = build_event_list(update)
        await update.message.reply_text(text, reply_markup=keyboard)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    await update.message.reply_text(
        "Use /start to test this bot. Use /clear to clear the stored data so that you can see "
        "what happens, if the button data is not available. "
    )


async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Clears the callback data cache"""
    context.bot.callback_data_cache.clear_callback_data()
    context.bot.callback_data_cache.clear_callback_queries()
    await update.effective_message.reply_text("All clear!")


async def list_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()
    # Get the data from the callback_data.
    # If you're using a type checker like MyPy, you'll have to use typing.cast
    # to make the checker get the expected type of the callback_data
    number, number_list = cast(Tuple[int, List[int]], query.data)
    # append the number to the list
    number_list.append(number)

    await query.edit_message_text(
        text=f"So far you've selected {number_list}. Choose the next item:",
        reply_markup=build_keyboard(number_list),
    )

    # we can delete the data stored for the query, because we've replaced the buttons
    context.drop_callback_data(query)


async def handle_invalid_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Informs the user that the button is no longer available."""
    await update.callback_query.answer()
    await update.effective_message.edit_text(
        "Sorry, I could not process this button click 😕 Please send /start to get a new keyboard."
    )


def main():
    """Run the bot."""
    # Create the Application and pass it the bot's token.
    application = (
        Application.builder()
        .token("5357075423:AAFij_e9Y_KxGvHfpHiJ-2znH9Cuo4Lf-xg")
        .arbitrary_callback_data(True)
        .build()
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("clear", clear))
    application.add_handler(
        CallbackQueryHandler(handle_invalid_button, pattern=InvalidCallbackData)
    )
    application.add_handler(CallbackQueryHandler(list_button))

    # Run the bot
    application.run_polling()


if __name__ == "__main__":
    main()