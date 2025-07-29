"""
Idea:

Basic CLI interaction (using typer)
Should have some command allowing to generate cards

Arguments:
    topic : str (required)
    num_of_cards : int (optional)
"""
import typer
import anki_scraper.deck_generation as dg

app = typer.Typer()

@app.command()
def generate(topic: str, num_of_cards: int):
    new_deck = dg.make_cards(topic, num_of_cards)

@app.command()
def null(): 
    pass

if __name__ == "__main__":
    app()