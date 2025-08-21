import typer

from pathlib import Path
from appdirs import user_config_dir

import anki_scraper.anki_flashcards as dg
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
    template_path = Path("prompts/prompt.txt")
    template = template_path.read_text(encoding="utf-8").strip()

    prompt_text = template.format(
        topic=topic,
        topic_description=(description or ""),
        num_cards=num_of_cards
    )
    raw_response = dg.prompt_gpt_to_create_flashcards(prompt_text)

    cards = dg.parse_flashcards_from_jsonl(raw_response)
    
@app.command("set-output")
def set_output(new_dir: Path = typer.Argument(
        ...,
        help="Overwrite the default output path",
    )):
    io.save_output_dir(new_dir)

if __name__ == "__main__":
    app()