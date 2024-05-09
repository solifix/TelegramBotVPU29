from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler, CommandHandler, ContextTypes, MessageHandler, filters, \
    CallbackQueryHandler

from handlers.base_handler import BaseHandler

GENDER, PHOTO, AGE = range(3)


class FirstConversationHandler(BaseHandler):
    @classmethod
    def register(cls, app):
        conversation_handler = ConversationHandler(
            entry_points=[CommandHandler('begin', cls.begin)],
            states={
                GENDER: [MessageHandler(filters.Regex('^(Boy|Girl)$'), cls.gender)],
                PHOTO: [MessageHandler(filters.PHOTO, cls.photo)],
                AGE: [CallbackQueryHandler(cls.age)],
            },
            fallbacks=[CommandHandler('exit', cls.exit)]
        )

        app.add_handler(conversation_handler)

    @staticmethod
    async def begin(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(f'Hello {update.effective_user.first_name}! Are you a Boy or a Girl?')

        return GENDER

    @staticmethod
    async def exit(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(f'Exit from conversation')

        return ConversationHandler.END

    @staticmethod
    async def gender(update: Update, context: ContextTypes.DEFAULT_TYPE):
        gender = update.message.text # Boy or Girl

        context.user_data['gender'] = gender

        await update.message.reply_text(f'You are a {gender}. Share your photo, please!')

        return PHOTO

    @staticmethod
    async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Sends a message with three inline buttons attached."""
        keyboard = []
        number = 1

        for i in range(10):
            row = []

            for j in range(5):
                row.append(InlineKeyboardButton(f"{number}", callback_data=f"{number}"))
                number += 1

            keyboard.append(row)
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text("Thank you for your photo! How old are you?", reply_markup=reply_markup)

        return AGE

    @staticmethod
    async def age(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Parses the CallbackQuery and updates the message text."""
        query = update.callback_query

        # CallbackQueries need to be answered, even if no notification to the user is needed
        # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
        await query.answer()

        age = query.data

        context.user_data['age'] = age

        await query.edit_message_text(text=f"You are a {context.user_data['gender']}. Your age is: {context.user_data['age']}")

        return ConversationHandler.END