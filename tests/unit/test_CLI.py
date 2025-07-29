from anki_scraper.cli import app
from typer.testing import CliRunner

from anki_scraper.models import Card

runner = CliRunner()

def test_generate_happy_path(monkeypatch, tmp_path):
    card1 = Card(front="What is Python?", back="A programming language.")
    assert card1.front == "What is Python?"
    assert card1.back == "A programming language."

def test_generate_missing_args():
    result = runner.invoke(app, ["generate"])
    assert result.exit_code != 0