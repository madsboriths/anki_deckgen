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

