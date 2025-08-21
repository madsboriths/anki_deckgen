import genanki as gk
import random, json, re
import anki_scraper.models as models
from anki_scraper.anki_connect import invoke
from anki_scraper.models import Flashcard
from typing import List, Tuple
from pathlib import Path
from openai import OpenAI
import os

deck_id = random.randint(1, 2**31 - 1)

API_KEY = os.environ["OPENAI_API_KEY"]
client = OpenAI(api_key=API_KEY)

def parse_flashcards_from_jsonl(jsonl: str) -> List[Flashcard]:
    m = re.search(r"```jsonl\s*(.+?)\s*```", jsonl, flags=re.DOTALL | re.IGNORECASE)
    if not m:
        m = re.search(r"```\w*\s*(.+?)\s*```", jsonl, flags=re.DOTALL)
    if not m:
        raise ValueError("No fenced code block found in response.")

    block = m.group(1).strip()
    lines = [ln for ln in block.splitlines() if ln.strip()]

    cards: List[Flashcard] = []
    for ln in lines:
        txt = ln.strip().rstrip(",")
        try:
            obj = json.loads(txt)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON line: {txt}") from e
                        
        deck = obj.get("deck")
        front = obj.get("front")
        back  = obj.get("back")
        if not isinstance(front, str) or not isinstance(back, str):
            raise ValueError(f"Missing 'deck'/'front'/'back' fields in: {obj}")

        cards.append(Flashcard(
            deck_name=deck,
            front=front,
            back=back)
        )
    return cards

def add_cards_to_respective_decks(flashcards: List[Flashcard]) -> None:
    genanki_specific_decks = [deck_name for deck_name in invoke("deckNames") if "GK" in deck_name]
    for flashcard in flashcards:
        note = {
            "deckName": flashcard.deck_name,
            "modelName": "Basic",
            "fields": {
                "Front": flashcard.front,
                "Back": flashcard.back
            }
        }
        if flashcard.deck_name in genanki_specific_decks:
            invoke("addNote", note=note)
        else:
            invoke("createDeck", deck=flashcard.deck_name)
            invoke("addNote", note=note)
    invoke("sync")
    return f"Added {len(flashcards)} cards to respective decks."

# def create_flashcard(question: str, answer: str) -> gk.Note:
#     return gk.Note(
#         model=models.STANDARD_MODEL,
#         fields=[question, answer]
#     )

# def create_flashcard_deck(flashcards: List[Tuple[str, str, str]], deck_name: str) -> None:
#     new_deck = gk.Deck(deck_id, deck_name)
#     for question, answer in flashcards:
#         flashcard = create_flashcard(question, answer)
#         new_deck.add_note(flashcard)
#     return new_deck

