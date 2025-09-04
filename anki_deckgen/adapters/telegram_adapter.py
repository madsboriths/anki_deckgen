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

    # async def generate_flashcards_by_user_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #     prompt_path = Path("prompts/telegram_prompt.txt")
    #     system_prompt = prompt_path.read_text(encoding="utf-8").strip()
        
    #     parsed_args = json.loads(execute_gpt_query(system_prompt=system_prompt, user_prompt=update.message.text))

    #     print(f"Parsed arguments: {parsed_args}")

    #     topic = parsed_args.get("topic").strip()
    #     description = parsed_args.get("topic_description").strip()
    #     num_cards = parsed_args.get("num_cards", 1)
    #     deck = parsed_args.get("deck")

    #     gk_decks = [deck_name for deck_name in execute_anki_action("deckNames") if "GK" in deck_name]
        
    #     prompt_path = Path("prompts/prompt.txt")
    #     system_prompt = prompt_path.read_text(encoding="utf-8").strip()
    #     user_prompt = f"""
    #         topic: {topic},
    #         description: {description or ""},
    #         number of cards: {num_cards},
    #         Available decks: {', '.join(gk_decks)},
    #         deck to use: {deck or "Default"}
    #     """

    #     response_string = execute_gpt_query(system_prompt=system_prompt, user_prompt=user_prompt)
    #     flashcards = parse_flashcards_from_jsonl(response_string) 
    #     response = add_cards_to_respective_decks(flashcards)
        
    #     await context.bot.send_message(
    #         chat_id=update.effective_chat.id,
    #         text=response
    #     )