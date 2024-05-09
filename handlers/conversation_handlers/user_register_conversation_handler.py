from handlers.base_handler import BaseHandler
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, \
    InlineKeyboardMarkup
from telegram.ext import ConversationHandler, CommandHandler, ContextTypes, MessageHandler, filters, \
    CallbackQueryHandler

from models.user import User

STATE_FIRST_NAME, STATE_LAST_NAME, STATE_EMAIL, STATE_PHONE_NUMBER = range(4)


class UserRegConversationHandler(BaseHandler):
    @classmethod
    def register(cls, app):
        conversation_handler = ConversationHandler(
            entry_points=[CommandHandler('user_register', cls.user_register)],
            states={
                STATE_FIRST_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, cls.state_first_name)],
                STATE_LAST_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, cls.state_last_name)],
                STATE_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, cls.email)],
                STATE_PHONE_NUMBER: [
                    MessageHandler(filters.CONTACT, cls.state_phone_number),
                    MessageHandler(filters.TEXT & ~filters.COMMAND, cls.state_phone_number),

                ]
            },
            fallbacks=[CommandHandler('exit', cls.exit)]
        )

        app.add_handler(conversation_handler)

    @staticmethod
    async def user_register(update: Update, context: ContextTypes.DEFAULT_TYPE):

        await update.message.reply_text(f'Hello {update.effective_user.first_name}! For regging enter your name')
        return STATE_FIRST_NAME

    @staticmethod
    async def exit(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(f'Exit from conversation')

        return ConversationHandler.END

    @staticmethod
    async def state_first_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
        first_name = update.message.text
        context.user_data["first_name"] = first_name
        await update.message.reply_text(f'Next step, enter your last name')
        return STATE_LAST_NAME

    @staticmethod
    async def state_last_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
        last_name = update.message.text
        context.user_data["last_name"] = last_name

        contact_keyboard = KeyboardButton("Share contact", request_contact=True)
        keyboard = [
            [contact_keyboard],

        ]
        reply_markup = ReplyKeyboardMarkup(keyboard)
        await update.message.reply_text(f'Next step, Share or enter your email', reply_markup=reply_markup)
        return STATE_EMAIL

    @staticmethod
    async def email(update: Update, context: ContextTypes.DEFAULT_TYPE):
        email = update.message.text
        context.user_data["email"] = email
        await update.message.reply_text(f'Next step, enter your phone number')

        return STATE_PHONE_NUMBER

    @classmethod
    async def state_phone_number(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.contact:
            phone_number = update.message.contact.phone_number
        else:
            phone_number = update.message.text
        context.user_data["phone_number"] = phone_number

        first_name = context.user_data['first_name']
        last_name = context.user_data['last_name']
        email = context.user_data['email']

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number
        )
        cls.session.add(new_user)
        cls.session.commit()

        await update.message.reply_text(
            f"Very well, your first name: {first_name}, \n"
            f"your last name: {last_name},\n"
            f"your last email: {email},\n"
            f"your phone number: {phone_number}."
        )

        return ConversationHandler.END
