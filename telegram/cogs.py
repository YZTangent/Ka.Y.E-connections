import re
from telegram import Update
from telegram.ext import ContextTypes
#
# MARKDOWN_SPECIAL_CHAR = ['\\', '`', '*', '_', '{', '}', '[', ']', '(', ')', '#', '+', '-', '.', '!']
#
# def handle_special_markdown_char(string):
#     return string.replace(i for i in MARKDOWN_SPECIAL_CHAR)

# print(handle_special_markdown_char("~*-{}[]"))


def escape_markdown(text: str, version: int = 1, entity_type: str = None) -> str:
    """
    Helper function to escape telegram markup symbols.
    Args:
        text (:obj:`str`): The text.
        version (:obj:`int` | :obj:`str`): Use to specify the version of telegrams Markdown.
            Either ``1`` or ``2``. Defaults to ``1``.
        entity_type (:obj:`str`, optional): For the entity types ``PRE``, ``CODE`` and the link
            part of ``TEXT_LINKS``, only certain characters need to be escaped in ``MarkdownV2``.
            See the official API documentation for details. Only valid in combination with
            ``version=2``, will be ignored else.
    """

    escape_chars = r'_*[]()~`>#+-=|{}.!'

    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)


def private_check(private_func, group_func):
    async def inner(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.chat.type == 'private':
            result = await private_func(update, context)

            return result
        else:
            result = await group_func(update, context)

            return result

    return inner
