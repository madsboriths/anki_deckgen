from anki_scraper.cli import app
from typer.testing import CliRunner

runner = CliRunner()

def test_generate_creates_apkg(tmp_path, monkeypatch):
    result = runner.invoke(app, ["generate", "types", "--output", str(tmp_path/"d.apkg")])
    assert result.exit_code == 0
    assert (tmp_path/"d.apkg").exists()