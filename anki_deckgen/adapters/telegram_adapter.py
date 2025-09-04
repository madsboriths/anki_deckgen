from telegram.ext import ContextTypes, ApplicationBuilder, MessageHandler, filters, Application
from telegram import Update

class TelegramAdapter:
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.application = ApplicationBuilder().token(self.api_token).build()

    def start(self, on_message):
        async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
            user_message = update.message.text or ""
            response = on_message(user_message)
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=response or ""
            )

        anki_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
        
        self.application.add_handler(anki_handler)
        self.application.run_polling()