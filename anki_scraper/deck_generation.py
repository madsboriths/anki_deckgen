import genanki as gk
import random, json, re

import anki_scraper.models as models
from typing import List, Tuple

deck_id = random.randint(1, 2**31 - 1)

from pathlib import Path
from openai import OpenAI
import os

API_KEY = os.environ["OPENAI_API_KEY"]
client = OpenAI(api_key=API_KEY)

def prompt_openai(prompt: str) -> str:
    try:
        response = client.responses.create(
            model="gpt-5-nano",
            input=f"{prompt}\n\nHTML:\n{prompt}",
        )
    except Exception as e:
        raise RuntimeError(f"Failed to prompt: {e}") from e
    return response.output_text.strip()

def parse_response(response: str) -> List[Tuple[str, str]]:
    m = re.search(r"```jsonl\s*(.+?)\s*```", response, flags=re.DOTALL | re.IGNORECASE)
    if not m:
        m = re.search(r"```\w*\s*(.+?)\s*```", response, flags=re.DOTALL)
    if not m:
        raise ValueError("No fenced code block found in response.")

    block = m.group(1).strip()
    lines = [ln for ln in block.splitlines() if ln.strip()]

    cards: List[Tuple[str, str]] = []
    for ln in lines:
        txt = ln.strip().rstrip(",")
        try:
            obj = json.loads(txt)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON line: {txt}") from e

        front = obj.get("front")
        back  = obj.get("back")
        if not isinstance(front, str) or not isinstance(back, str):
            raise ValueError(f"Missing 'front'/'back' fields in: {obj}")

        cards.append((front, back))
    return cards

def create_flashcard(question: str, answer: str) -> gk.Note:
    return gk.Note(
        model=models.STANDARD_MODEL,
        fields=[question, answer]
    )

def create_flashcard_deck(flashcards: List[Tuple[str, str]], topic: str) -> gk.Deck:
    new_deck = gk.Deck(deck_id, "Generated Deck")
    for question, answer in flashcards:
        flashcard = create_flashcard(question, answer)
        new_deck.add_note(flashcard)
    return new_deck

if __name__ == "__main__":
    topic = "Ball Python"
    description = """
    A ball python is a non-venomous constrictor snake native to sub-Saharan Africa.
    They are known for their docile nature and distinctive pattern, which resembles a ball when coiled.
    Ball pythons are popular pets due to their manageable size and relatively easy care requirements.
    They typically grow to about 3 to 5 feet in length and can live for over 20 years in captivity.
    Ball pythons are primarily nocturnal and feed on small mammals, such as mice and rats.
    They are also known for their unique behavior of balling up when threatened, hence their name.
    """
    template_path = Path("prompts/prompt.txt")
    template = template_path.read_text(encoding="utf-8").strip()

    prompt_text = template.format(
        topic=topic,
        topic_description=(description or ""),
        num_cards=5
    )
    raw_response = prompt_openai(prompt_text)

    # with open("raw_response.txt", "r", encoding="utf-8") as f:
    #     raw_response = f.read().strip()
    cards = parse_response(raw_response)
    deck = create_flashcard_deck(cards, topic=topic)
    
    gk.Package(deck).write_to_file(Path("generated_decks") / f"{topic}.apkg")