import os, logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from anki_scraper.deck_generation import prompt_gpt_to_create_flashcards, extract_flashcard_pairs, create_flashcard_deck
from pathlib import Path
from openai import OpenAI
import json
import genanki as gk

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
API_KEY = os.environ["OPENAI_API_KEY"]

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

client = OpenAI(api_key=API_KEY)

def prompt_gpt_to_prepare_arguments(user_message: str) -> str:
    
    prompt_path = Path("prompts/telegram_prompt.txt")
    system_prompt = prompt_path.read_text(encoding="utf-8").strip()

    response = client.responses.create(
        model="gpt-5-nano",
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ]
    )

    parsed_response = json.loads(response.output_text.strip())

    topic = parsed_response.get("topic", "").strip()
    topic_description = parsed_response.get("topic_description", "").strip()
    num_cards = parsed_response.get("num_cards", 3)

    result = {
        "topic": topic,
        "topic_description": topic_description,
        "num_cards": num_cards,
    }

    return json.dumps(result, ensure_ascii=False)

async def create_cards(update: Update, context: ContextTypes.DEFAULT_TYPE):
    parsed_args = prompt_gpt_to_prepare_arguments(update.message.text)
    
    topic = json.loads(parsed_args).get("topic", "").strip()
    description = json.loads(parsed_args).get("topic_description", "").strip()
    num_cards = json.loads(parsed_args).get("num_cards", 3)

    print(f"Creating deck for topic: {topic}, description: {description}, num_cards: {num_cards}")

    template_path = Path("prompts/prompt.txt")
    template = template_path.read_text(encoding="utf-8").strip()
    prompt_text = template.format(
        topic=topic,
        topic_description=(description or ""),
        num_cards=num_cards
    )

    response = prompt_gpt_to_create_flashcards(prompt_text)
    flashcards = extract_flashcard_pairs(response)

    deck = create_flashcard_deck(flashcards, topic=topic)
    gk.Package(deck).write_to_file(Path("generated_decks") / f"{topic}.apkg")

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"""
            Deck for topic '{topic}' with {num_cards} cards has been created successfully!"""
    )

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    anki_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), create_cards)
    application.add_handler(anki_handler)

    application.run_polling()