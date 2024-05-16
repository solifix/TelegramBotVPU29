from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, CommandHandler

from handlers.base_handler import BaseHandler


class HtmlHandler(BaseHandler):
    @classmethod
    def register(cls, app):
        app.add_handler(CommandHandler('html', cls.callback))

    @staticmethod
    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        message = (
           "<b>Hello world!</b> \n"
           "<a href=\"https://vpu29.lviv.ua/\">Сайт ВПУ29</a> \n"
        )
        await update.message.reply_text(message, parse_mode=ParseMode.HTML)
