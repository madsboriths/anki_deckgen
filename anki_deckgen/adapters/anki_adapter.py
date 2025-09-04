import json
import urllib.request
import requests
from anki_deckgen.core.models import Flashcard
from typing import List

def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

def is_anki_running():
    try:
        response = requests.post("http://127.0.0.1:8765", json={"action": "version", "version": 6}, timeout=1)
        if response.status_code == 200:
            return True
    except requests.exceptions.RequestException:
        return False

def execute_anki_action(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']

def add_cards_to_respective_decks(flashcards: List[Flashcard]) -> None:
    genanki_specific_decks = [deck_name for deck_name in execute_anki_action("deckNames") if "GK" in deck_name]
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
            execute_anki_action("addNote", note=note)
        else:
            execute_anki_action("createDeck", deck=flashcard.deck_name)
            execute_anki_action("addNote", note=note)
    execute_anki_action("sync")
    return f"Added {len(flashcards)} cards to respective decks."