import genanki as gk

import random

STANDARD_MODEL = gk.Model(
  random.randrange(1 << 30, 1 << 31),
  'Standard Model',
  fields=[
    {'name': 'Question'},
    {'name': 'Answer'},
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': '{{Question}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
    },
  ],
  css="""
  .card {
    font-family: arial;
    font-size: 35px;
    text-align: center;
    color: black;
    background-color: white;
  }
  """)

class Flashcard:
    def __init__(self, deck_name: str, front: str, back: str):
        self.deck_name = deck_name
        self.front = front
        self.back = back

    def __repr__(self):
        return f"Flashcard(deck_name={self.deck_name!r}, question={self.front!r}, answer={self.back!r})"

    def to_dict(self):
        return {
            "deck_name": self.deck_name,
            "question": self.front,
            "answer": self.back
        }