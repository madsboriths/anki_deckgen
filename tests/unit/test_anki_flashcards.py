from anki_deckgen.core.flashcard_logic import create_or_update_flashcard_deck

def test_add_cards_to_deck():
    flashcards ="""
        [
            {"front": "What is Python?", "back": "A programming language."},
            {"front": "What is a list?", "back": "A collection of items in a particular order."}
        ]
    """
    deck_name = "Python Basics"
    create_or_update_flashcard_deck(flashcards, deck_name)