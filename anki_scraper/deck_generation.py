from anki_scraper.models import Card

def make_cards(topic: str, num_of_cards: int = 200):
    return Card(topic, num_of_cards)    