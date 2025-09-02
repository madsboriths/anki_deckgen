import os, logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from anki_scraper.anki_flashcards import parse_flashcards_from_jsonl, add_cards_to_respective_decks
from .anki_connect import invoke
from pathlib import Path
from openai import OpenAI
from .openai_client import prompt_gpt
import json
import genanki as gk
from typing import List, Tuple

API_KEY = os.environ["OPENAI_API_KEY"]
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

client = OpenAI(api_key=API_KEY)

async def generate_flashcards_by_user_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt_path = Path("prompts/telegram_prompt.txt")
    system_prompt = prompt_path.read_text(encoding="utf-8").strip()
    
    parsed_args = json.loads(prompt_gpt(system_prompt=system_prompt, user_prompt=update.message.text))

    print(f"Parsed arguments: {parsed_args}")

    topic = parsed_args.get("topic").strip()
    description = parsed_args.get("topic_description").strip()
    num_cards = parsed_args.get("num_cards", 1)

    gk_decks = [deck_name for deck_name in invoke("deckNames") if "GK" in deck_name]
    
    prompt_path = Path("prompts/prompt.txt")
    system_prompt = prompt_path.read_text(encoding="utf-8").strip()
    user_prompt = f"""
        topic: {topic},
        description: {description or ""},
        number of cards: {num_cards},
        Available decks: {', '.join(gk_decks)}
    """

    response_string = prompt_gpt(system_prompt=system_prompt, user_prompt=user_prompt)
    flashcards = parse_flashcards_from_jsonl(response_string) 
    response = add_cards_to_respective_decks(flashcards)
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response
    )

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    anki_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), generate_flashcards_by_user_prompt)
    application.add_handler(anki_handler)

    application.run_polling()