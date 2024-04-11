from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from handlers.base_handler import BaseHandler


class ByHandler(BaseHandler):
    @classmethod
    def register(cls, app):
        hello_handler = CommandHandler('by', cls.callback)
        app.add_handler(hello_handler)

    @staticmethod
    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(f'By {update.effective_user.first_name}')
