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
ops = { "+": operator.add, "-": operator.sub }


def create_event():

    ACTIVITY, LOCATION, STARTTIME, DURATION = range(4)
    event_info = {}

    async def create_event_private(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Starting point of an event creation which asks for a description of the event."""
        await update.message.reply_text(
            "activity"
        )

        return ACTIVITY

    async def create_event_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(
            "Hi! Please create your event in a private message with me. "
        )

    async def activity(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Stores the activity description and asks for a location."""
        event_info["activity"] = update.message.text
        await update.message.reply_text("location")

        return LOCATION

    async def location_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        event_info["longitude"] = update.message.location.longitude
        event_info["latitude"] = update.message.location.latitude
        await update.message.reply_text("start time")

        return STARTTIME

    async def location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        event_info["location"] = update.message.text
        await update.message.reply_text("start time")

        return STARTTIME

    async def skip_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await update.message.reply_text(
            "start time"
        )

        return STARTTIME

    async def start_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        try:
            date, time, timezone = update.message.text.split()
            year, month, day = date.split("/")
            hour = ops[timezone[0]](int(time[0:2]), int(timezone[1]))
            minute = int(time[2:])
            ts = datetime(int(year), int(month), int(day), hour, minute).isoformat()
            event_info["starttime"] = update.message.text
        except ValueError:
            await update.message.reply_text(
                "Invalid Date/Time!"
            )
            return STARTTIME
        await update.message.reply_text("duration")

        return DURATION

    async def duration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        event_info["duration"] = update.message.text
        user_id = update.message.from_user.id
        event_info["creatorID"] = supa.get_user_uuid(TeleID=user_id)
        await supa.send_event(event_info)
        await update.message.reply_text("submitted")

        return ConversationHandler.END

    async def skip_duration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        user_id = update.message.from_user.id
        event_info["creatorID"] = supa.get_user_uuid(TeleID=user_id)
        await supa.send_event(event_info)
        await update.message.reply_text(
            "submitted"
        )

        return ConversationHandler.END

    async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Cancels and ends the conversation."""
        user = update.message.from_user
        await update.message.reply_text(
            "cancelled"
        )

        return ConversationHandler.END

    return ConversationHandler(
        entry_points=[CommandHandler("createevent", private_check(create_event_private, create_event_group))],
        states={
            ACTIVITY: [MessageHandler(filters.TEXT, activity)],
            LOCATION: [
                MessageHandler(filters.LOCATION, location_info),
                MessageHandler(filters.TEXT, location),
                CommandHandler("skip", skip_location),
            ],
            STARTTIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, start_time)],
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
        .token("5357075423:AAFij_e9Y_KxGvHfpHiJ-2znH9Cuo4Lf-xg")
        .arbitrary_callback_data(True)
        .build()
    )

    application.add_handler(create_event())

    # Run the bot
    application.run_polling()