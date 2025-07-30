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

import anki_scraper.fileio as io

import toml

from pathlib import Path
from appdirs import user_config_dir

app = typer.Typer()
    
# default_option = IO.load_output_dir()

@app.command()
def generate(topic: str, num_of_cards: int, 
             new_dir: Path = typer.Option(None, "--output", "-o",
                                        help="Where to write the .apkg. If unset, uses your config or CWD.")):
    if new_dir is not None:
        io.save_output_dir(new_dir)

    new_deck = dg.make_cards(topic, num_of_cards)
    print(f"Generated {num_of_cards} cards about {topic}")

@app.command("set-output")
def set_output(new_dir: Path = typer.Argument(
        ...,
        help="Overwrite the default output path",
    )):
    io.save_output_dir(new_dir)

if __name__ == "__main__":
    app()