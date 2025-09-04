from openai import OpenAI

from anki_deckgen.core.models import Message
from ..adapters.openai_adapter import OpenAIAdapter
from .flashcard_logic import parse_flashcards_from_jsonl
import os

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

def handle_user_request(raw_user_message: Message):
    client = OpenAI(api_key=OPENAI_API_KEY)
    llm = OpenAIAdapter(client, "gpt-5-nano")

    ## 1: decide strategy 
    with open("prompts/decision_prompt.txt", "r", encoding="utf-8") as f:
        decision_system_prompt = f.read().strip()
    decision = llm.execute_gpt_query(decision_system_prompt, raw_user_message)

    ## 2: create flashcards
    with open("prompts/flashcard_prompt.txt", "r", encoding="utf-8") as f:
        flashcard_system_prompt = f.read().strip()
    
    decks = None
    user_prompt = f"""
        mode:{decision},
        text:{raw_user_message}, 
        available decks:{decks}
    """

    flashcards_jsonl = llm.execute_gpt_query(flashcard_system_prompt, raw_user_message)
    flashcards = parse_flashcards_from_jsonl(flashcards_jsonl)
    print(flashcards)

    ## 3: upload to anki
    
# handle_user_request("I want 2 cards about giraffes!!!")