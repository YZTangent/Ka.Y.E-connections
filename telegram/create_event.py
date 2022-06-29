from connection import supabaseinteraction as supa
from datetime import datetime
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from cogs import private_check
import operator
import sys

sys.path.append('.')
ops = {"+": operator.add, "-": operator.sub}

def create_event():
    ACTIVITY, DESCRIPTION, LOCATION, STARTTIME, DURATION = range(5)
    event_info = {}

    async def create_event_private(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Starting point of an event creation which asks for a description of the event."""
        await update.message.reply_text(
            "Hi! Please tell me the name of your event!"
        )

        return ACTIVITY

    async def create_event_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(
            "Hi! Please create your event in a private message with me. "
        )

    async def activity(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Stores the activity description and asks for a location."""
        event_info["activity"] = update.message.text
        await update.message.reply_text(
            "That sounds fun! Now gimme more details about this event so your guests can know what to expect! "
            "Or, you can skip this step with /skip.")

        return DESCRIPTION

    async def description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Stores the activity description and asks for details of the event."""
        event_info["description"] = update.message.text
        await update.message.reply_text(
            "Now, please tell me the location of your event!"
            "\nYou can do so either by telling me directly, or you can send"
            "a location in your attachment menu on Telegram mobile."
            "\nYou can skip this step by pressing /skip.")

        return LOCATION

    async def skip_description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(
            "Now, please tell me the location of your event!"
            "\nYou can do so either by telling me directly, or you can send"
            "a location in your attachment menu on Telegram mobile."
            "\nYou can skip this step by pressing /skip.")

        return LOCATION

    async def location_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        event_info["longitude"] = update.message.location.longitude
        event_info["latitude"] = update.message.location.latitude
        await update.message.reply_text(
            "When does your event start? Please let me know in YYYY/MM/DD TTTT +UTC format"
            "\nYou can either decide it now, or leave it empty"
            "with /skip "
            "and let the bot suggest an optimal time after gathering everyone's RSVP!"
            "\nHowever, please bear in mind that if you confirm the starting time now,"
            "the bot will not be able to suggest timings for this event if you change"
            "your mind later.")

        return STARTTIME

    async def location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        event_info["location"] = update.message.text
        await update.message.reply_text(
            "When does your event start? Please let me know in YYYY/MM/DD TTTT +UTC format"
            "\nYou can either decide it now, or leave it empty"
            "with /skip "
            "and let the bot suggest an optimal time after gathering everyone's RSVP!"
            "\nHowever, please bear in mind that if you confirm the starting time now,"
            "the bot will not be able to suggest timings for this event if you change"
            "your mind later.")

        return STARTTIME

    async def skip_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await update.message.reply_text(
            "When does your event start? Please let me know in YYYY/MM/DD TTTT +UTC format."
            "\nYou can either decide it now, or leave it empty"
            "with /skip "
            "and let the bot suggest an optimal time after gathering everyone's RSVP!"
            "\nHowever, please bear in mind that if you confirm the starting time now,"
            "the bot will not be able to suggest timings for this event if you change"
            "your mind later."
        )

        return STARTTIME

    async def start_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        try:
            date, time, timezone = update.message.text.split()
            year, month, day = date.split("/")
            hour = ops[timezone[0]](int(time[0:2]), int(timezone[1])) % 24
            minute = int(time[2:])
            ts = datetime(int(year), int(month), int(day), hour, minute).isoformat()
            event_info["starttime"] = update.message.text
            event_info["finalised"] = True
        except ValueError:
            await update.message.reply_text(
                "Invalid Date/Time!"
            )
            return STARTTIME
        await update.message.reply_text(
            "How long will this event be in hours? Just an approximation will do if it's not confirmed yet :)"
        )

        return DURATION

    async def skip_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        event_info["finalised"] = False
        await update.message.reply_text(
            "How long will this event be in hours? Just an approximation will do if it's not confirmed yet :)"
        )

        return DURATION

    async def duration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        event_info["duration"] = update.message.text
        user_id = update.message.from_user.id
        event_info["creatorID"] = await supa.get_user_uuid(TeleID=user_id)
        await supa.send_event(event_info)
        await update.message.reply_text(
            "Your event has been created! You now can send RSVPs for this event by adding me to your group and then "
            "sending the /send_rsvp command."
        )

        return ConversationHandler.END

    async def skip_duration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        user_id = update.message.from_user.id
        event_info["creatorID"] = await supa.get_user_uuid(TeleID=user_id)
        await supa.send_event(event_info)
        await update.message.reply_text(
            "Your event has been created! You now can send RSVPs for this event by adding me to your group and then "
            "sending the /send_rsvp command."
        )

        return ConversationHandler.END

    async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Cancels and ends the conversation."""
        user = update.message.from_user
        await update.message.reply_text(
            "Aww :( See you again soon!"
        )

        return ConversationHandler.END

    return ConversationHandler(
        entry_points=[CommandHandler("createevent", private_check(create_event_private, create_event_group))],
        states={
            ACTIVITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, activity)],
            DESCRIPTION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, description),
                CommandHandler("skip", skip_description)
            ],
            LOCATION: [
                MessageHandler(filters.LOCATION, location_info),
                MessageHandler(filters.TEXT & ~filters.COMMAND, location),
                CommandHandler("skip", skip_location),
            ],
            STARTTIME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, start_time),
                CommandHandler("skip", skip_time),
            ],
            DURATION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, duration),
                CommandHandler("skip", skip_duration),
            ],

        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )


if __name__ == "__main__":
    application = (
        Application.builder()
            .token('TELE_BOT_TOKEN')
            .arbitrary_callback_data(True)
            .build()
    )

    application.add_handler(create_event())

    # Run the bot
    application.run_polling()
