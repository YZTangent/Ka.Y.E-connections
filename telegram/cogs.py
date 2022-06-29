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

def private_check(private_func, group_func):
    async def inner(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.chat.type == 'private':
            result = await private_func(update, context)

            return result
        else:
            result = await group_func(update, context)

            return result

    return inner
