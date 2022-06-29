import logging
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
from create_event import create_event
from rsvp import send_rsvp, choose_rsvp, handle_rsvp

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

"""
-------------------------------------------- Element builders ----------------------------------------------------------
"""
def build_keyboard(current_list) -> InlineKeyboardMarkup:
    events = supa.get_event().data
    return InlineKeyboardMarkup.from_column(
        [InlineKeyboardButton(i['activity'], callback_data=("events", i)) for i in events]
    )





def build_rsvp_message(update: Update) -> InlineKeyboardMarkup:
    events = supa.get_event().data
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Yes", callback_data=("rsvp", True))],
        [InlineKeyboardButton("No", callback_data=("rsvp", False))],
    ])


"""
-------------------------------------------- Handlers ------------------------------------------------------------------
"""
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    return


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


async def handle_send_rsvp(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Informs the user that the button is no longer available."""
    print(update['callback_query'])
    await update.callback_query.answer()
    await update.effective_message.edit_text(
        "Sorry, I could not process this button click 😕 Please send /start to get a new keyboard."
    )

def main():
    """Run the bot."""
    # Create the Application and pass it the bot's token.
    application = (
        Application.builder()
<<<<<<< HEAD
        .token(os.getenv('TELE_BOT_TOKEN')) # Main bot
        # .token(os.getenv('TELE_BOT_TOKEN_TEST')) # Test bot
=======
        .token("5357075423:AAFij_e9Y_KxGvHfpHiJ-2znH9Cuo4Lf-xg")
>>>>>>> 395d8cb2c3c1400898f22bd9a3cab29557095b85
        .arbitrary_callback_data(True)
        .build()
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("clear", clear))
    # application.add_handler(
    #     CallbackQueryHandler(handle_invalid_button, pattern=InvalidCallbackData)
    # )
    application.add_handler(choose_rsvp())
    application.add_handler(create_event())
    application.add_handler(send_rsvp())
    application.add_handler(handle_rsvp())

    # Run the bot
    application.run_polling()


if __name__ == "__main__":
    main()