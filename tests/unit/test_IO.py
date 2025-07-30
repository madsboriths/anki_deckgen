from anki_scraper.cli import app
from anki_scraper.models import Card
import anki_scraper.cli as cli
import anki_scraper.fileio as io

from typer.testing import CliRunner

from pathlib import Path
import toml

import pytest

runner = CliRunner()

@pytest.fixture
def fake_config(tmp_path, monkeypatch):
    tmp_dir = tmp_path / "fake-anki-scraper"
    tmp_file = tmp_dir / "config.toml"
    monkeypatch.setattr(io, "CONFIG_DIR", tmp_dir)
    monkeypatch.setattr(io, "CONFIG_FILE", tmp_file)
    return tmp_file

def test_set_output_path_successfully(fake_config, monkeypatch):
    test_path = "./generated_decks"
    result = runner.invoke(app, ["set-output", test_path])

    assert result.exit_code == 0
    assert Path(io.CONFIG_FILE).exists()

    cfg = toml.loads(io.CONFIG_FILE.read_text())
    assert Path(cfg["output_dir"]) == Path(str(test_path))

def test_write_deck_successfully():
    pytest.fail("TODO")