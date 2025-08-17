import typer

from pathlib import Path
from appdirs import user_config_dir

import anki_scraper.deck_generation as dg
import anki_scraper.fileio as io

import genanki as gk

app = typer.Typer()
    
@app.command()
def generate(
    topic: str = typer.Argument(..., help="The topic for the flashcards"),
    num_of_cards: int = typer.Option(5, "--num-cards", "-n", help="Number of cards to generate"),
    description: str = typer.Option("", "--description", "-d", help="Description of the topic"),
             new_dir: Path = typer.Option(None, "--output", "-o",
                                        help="Where to write the .apkg. If unset, uses your config or CWD.")):
    # if new_dir is not None:
    #     io.save_output_dir(new_dir)
    # new_deck = dg.create_flashcard_deck(topic, num_of_cards, description)
    # io.write_deck(new_deck)
    # typer.echo(f"Generated {num_of_cards} cards about {topic}")

    # topic = "Ball Python"
    # description = """
    # A ball python is a non-venomous constrictor snake native to sub-Saharan Africa.
    # They are known for their docile nature and distinctive pattern, which resembles a ball when coiled.
    # Ball pythons are popular pets due to their manageable size and relatively easy care requirements.
    # They typically grow to about 3 to 5 feet in length and can live for over 20 years in captivity.
    # Ball pythons are primarily nocturnal and feed on small mammals, such as mice and rats.
    # They are also known for their unique behavior of balling up when threatened, hence their name.
    # """
    template_path = Path("prompts/prompt.txt")
    template = template_path.read_text(encoding="utf-8").strip()

    prompt_text = template.format(
        topic=topic,
        topic_description=(description or ""),
        num_cards=num_of_cards
    )
    raw_response = dg.prompt_openai(prompt_text)

    cards = dg.parse_response(raw_response)
    deck = dg.create_flashcard_deck(cards, topic=topic)
    
    gk.Package(deck).write_to_file(Path("generated_decks") / f"{topic}.apkg")

@app.command("set-output")
def set_output(new_dir: Path = typer.Argument(
        ...,
        help="Overwrite the default output path",
    )):
    io.save_output_dir(new_dir)

if __name__ == "__main__":
    app()