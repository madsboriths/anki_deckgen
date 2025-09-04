import genanki as gk
import random, json, re
from anki_deckgen.core.models import Flashcard
from typing import List

deck_id = random.randint(1, 2**31 - 1)

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

#  def add_cards_to_respective_decks(flashcards: List[Flashcard]) -> None:
#         genanki_specific_decks = [deck_name for deck_name in execute_anki_action("deckNames") if "GK" in deck_name]
#         for flashcard in flashcards:
#             note = {
#                 "deckName": flashcard.deck_name,
#                 "modelName": "Basic",
#                 "fields": {
#                     "Front": flashcard.front,
#                     "Back": flashcard.back
#                 }
#             }
#             if flashcard.deck_name in genanki_specific_decks:
#                 execute_anki_action("addNote", note=note)
#             else:
#                 execute_anki_action("createDeck", deck=flashcard.deck_name)
#                 execute_anki_action("addNote", note=note)
#         execute_anki_action("sync")
#         return f"Added {len(flashcards)} cards to respective decks."