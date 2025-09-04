from anki_deckgen.adapters.anki_adapter import AnkiFlashcardAdapter
from anki_deckgen.adapters.openai_adapter import OpenAIAdapter
from anki_deckgen.core.models import Message
from .flashcard_logic import parse_flashcards_from_jsonl

class Service:
    def __init__(self, llm_client: OpenAIAdapter, flashcard_client: AnkiFlashcardAdapter):
        self.llm = llm_client
        self.flashcard_client = flashcard_client

    def handle_user_request(self, raw_user_message: Message):
        with open("prompts/decision_prompt.txt", "r", encoding="utf-8") as f:
            decision_system_prompt = f.read().strip()
        decision = self.llm.execute_gpt_query(decision_system_prompt, raw_user_message)

        with open("prompts/flashcard_prompt.txt", "r", encoding="utf-8") as f:
            flashcard_system_prompt = f.read().strip()
        decks = self.flashcard_client.get_available_decks()
        user_prompt = f"""
            mode:{decision},
            text:{raw_user_message}, 
            available decks:{decks}
        """

        flashcards_jsonl = self.llm.execute_gpt_query(flashcard_system_prompt, user_prompt)
        flashcards = parse_flashcards_from_jsonl(flashcards_jsonl)
        response = self.flashcard_client.add_flashcards(flashcards=flashcards)
        return response
