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

import toml

from pathlib import Path
from appdirs import user_config_dir

app = typer.Typer()

CONFIG_DIR  = Path(user_config_dir("anki-scraper"))
CONFIG_FILE = CONFIG_DIR / "config.toml"

cfg_path = Path(CONFIG_FILE)
if cfg_path.exists():
    cfg = toml.loads(cfg_path.read_text())
    default_output = Path(cfg.get("output_dir"))
else:
    default_output = Path.cwd()

@app.command()
def generate(topic: str, num_of_cards: int, 
             new_dir: Path = typer.Option(default_output, "--output", "-o",
                                        help="Where to write the .apkg. If unset, uses your config or CWD.")):
    if new_dir is not None:
        set_output(new_dir=new_dir)

    new_deck = dg.make_cards(topic, num_of_cards)
    print(f"Generated {num_of_cards} cards about {topic}")

@app.command("set-output")
def set_output(new_dir: Path = typer.Argument(
        None,
        help="Where to write the .apkg. If unset, uses your config or CWD.",
    )):

    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        toml.dump({"output_dir": str()}, f)
    print(f"saved it to {new_dir}")

if __name__ == "__main__":
    app()