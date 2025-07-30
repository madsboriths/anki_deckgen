from dataclasses import dataclass

@dataclass
class Card:
    front: str
    back: str

@dataclass
class Deck:
    cards: list[Card]