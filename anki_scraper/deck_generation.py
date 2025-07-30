from anki_scraper.models import Card
import genanki as gk
import random

deck_id = random.randint(1, 2**31 - 1)

def make_cards(topic: str, num_of_cards: int = 200):
    new_deck = gk.Deck(deck_id, )
    return Card(topic, num_of_cards)    