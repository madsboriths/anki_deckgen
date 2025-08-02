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

from dataclasses import dataclass

@dataclass
class Card:
    front: str
    back: str

@dataclass
class Deck:
    cards: list[Card]
