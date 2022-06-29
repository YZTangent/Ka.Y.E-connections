from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)
from create_event import create_event
from rsvp import send_rsvp, choose_rsvp, handle_rsvp
from basic import start, help_command
import logging
import sys

sys.path.append('.')

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    """Run the bot."""
    # Create the Application and pass it the bot's token.
    application = (
        Application.builder()
        .token("5357075423:AAFij_e9Y_KxGvHfpHiJ-2znH9Cuo4Lf-xg")
        .arbitrary_callback_data(True)
        .build()
    )

    application.add_handler(start())
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(choose_rsvp())
    application.add_handler(create_event())
    application.add_handler(send_rsvp())
    application.add_handler(handle_rsvp())
    # application.add_handler(
    #     CallbackQueryHandler(handle_invalid_button, pattern=InvalidCallbackData)
    # )

    # Run the bot
    application.run_polling()


if __name__ == "__main__":
    main()