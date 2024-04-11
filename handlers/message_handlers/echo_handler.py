from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes, MessageHandler, filters

from handlers.base_handler import BaseHandler


class EchoHandler(BaseHandler):
    @classmethod
    def register(cls, app):
        contact_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, cls.callback)
        app.add_handler(contact_handler)

    @staticmethod
    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(update.message.text)
