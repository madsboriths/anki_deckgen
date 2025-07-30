from anki_scraper.models import Card
import genanki as gk
import random

import anki_scraper.models as models

deck_id = random.randint(1, 2**31 - 1)

def make_cards(topic: str, num_of_cards: int = 200):
    new_deck = gk.Deck(deck_id, topic)
    for i in range(num_of_cards):
        card = gk.Note(
            model=models.STANDARD_MODEL,
            fields=[f"Capital of Argentina no. {i}", "Buenos Aires"])  
        new_deck.add_note(card)
    return new_deck