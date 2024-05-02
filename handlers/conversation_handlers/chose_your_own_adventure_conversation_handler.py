from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler

from handlers.base_handler import BaseHandler

FOREST, TENT, HUNTING, BERRIES, TEMPLE, END = range(6)


class GameConversationHandler(BaseHandler):
    @classmethod
    def register(cls, app):
        conversation_handler = ConversationHandler(
            entry_points=[CommandHandler('game', cls.game)],
            states={
                FOREST: [MessageHandler(filters.Regex('^(Так|Ні)$'), cls.forest)],
                TENT: [MessageHandler(filters.Regex('^(Бігти|Здатись)$'), cls.tent)],
                HUNTING: [MessageHandler(filters.Regex('^(Спати|Шукати воду)$'), cls.hunting)],
            },
            fallbacks=[CommandHandler('exit', cls.exit)]
        )

        app.add_handler(conversation_handler)

    @staticmethod
    async def game(update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [KeyboardButton('Так'), KeyboardButton('Ні')],
        ]

        reply_text = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        await update.message.reply_text(f"Привіт {update.effective_user.first_name}! Чи бажаєте ви зіграти у гру?",reply_markup=reply_text)

        return FOREST

    @staticmethod
    async def exit(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(f'Ви вийшли з гри :^(')

        return ConversationHandler.END

    @staticmethod
    async def forest(update: Update, context: ContextTypes.DEFAULT_TYPE):
        answer = update.message.text
        if answer == 'Так':
            keyboard = [
                [KeyboardButton('Бігти'), KeyboardButton('Здатись')],
            ]

            reply_text = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
            await update.message.reply_text(
            f"""
            Ви мандрівник, який йшов через ліс але на вас напали вовки, та віддібрали вашу їжу.\nАле ви побачили будиночок і почали бігти до нього.    
            """, reply_markup=reply_text)

            return TENT
        elif answer == 'Ні':
            await update.message.reply_text(f'Ви обрали не грати в гру.')
            return ConversationHandler.END
        else:
            await update.message.reply_text(f'Ви обрали щоcь не те.')

    @staticmethod
    async def tent(update: Update, context: ContextTypes.DEFAULT_TYPE):
        answer = update.message.text
        if answer == 'Бігти':
            keyboard = [
                [KeyboardButton('Спати'), KeyboardButton('Шукати воду')],
            ]

            reply_text = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
            await update.message.reply_text(
            f"""
            Ви дійшли до будиночка, і побачили там їжу.\nВи були дуже голодні, що зайшли у будиночок і почали їсти.\n Ви наїлися, ви були дуже змучені і зневоднені. Що будете робити?     
            """, reply_markup=reply_text)
            return HUNTING
        elif answer == 'Здатись':
            await update.message.reply_text(f'Ви заблукали і вас покусали змії.')
            return ConversationHandler.END
        else:
            await update.message.reply_text(f'Ви обрали щоcь не те.')

    @staticmethod
    async def hunting(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        answer = update.message.text
        if answer == 'Полювати':
            keyboard = [
                [KeyboardButton("З'їсти"), KeyboardButton('Стриматись')]
            ]
            reply_text = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
            await update.message.reply_text('Ви розпочали полювання.', reply_markup=reply_text)
            return BERRIES
        else:
            await update.message.reply_text('Ви обрали щось не те.')




