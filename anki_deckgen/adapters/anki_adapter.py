import json
import urllib.request
import requests
from anki_deckgen.core.models import Flashcard
from typing import List

class AnkiFlashcardAdapter:
    def request(self, action, **params):
        return {'action': action, 'params': params, 'version': 6}

    def perform_action(self, action, **params):
        requestJson = json.dumps(self.request(action, **params)).encode('utf-8')
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
    
    def get_available_decks(self):
        return [deck_name for deck_name in self.perform_action("deckNames") if "GK" in deck_name]

    def add_flashcards(self, flashcards: List[Flashcard]) -> None:
        genanki_decks = self.get_available_decks()
        for flashcard in flashcards:
            note = {
                "deckName": flashcard.deck_name,
                "modelName": "Basic",
                "fields": {
                    "Front": flashcard.front,
                    "Back": flashcard.back
                }
            }
            if flashcard.deck_name in genanki_decks:
                self.perform_action("addNote", note=note)
            else:
                self.perform_action("createDeck", deck=flashcard.deck_name)
                self.perform_action("addNote", note=note)
        self.perform_action("sync")
        return f"Added {len(flashcards)} cards to respective decks."
    
    # def is_anki_running():
    #     try:
    #         response = requests.post("http://127.0.0.1:8765", json={"action": "version", "version": 6}, timeout=1)
    #         if response.status_code == 200:
    #             return True
    #     except requests.exceptions.RequestException:
    #         return False