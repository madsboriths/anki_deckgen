from typer.testing import CliRunner
from anki_deckgen.core.service import app

runner = CliRunner()

# @pytest.fixture
# def fake_decks(tmp_path, monkeypatch):
#     tmp_dir = tmp_path / "decks"
#     # tmp_file = tmp_dir / "config.toml"
#     monkeypatch.setattr(io, "CONFIG_DIR", tmp_dir)
#     # monkeypatch.setattr(io, "CONFIG_FILE", tmp_file)
#     return tmp_file

# def test_make_cards_successfully(fake_decks):
#     runner.invoke(app, ["generate", "AGI", 200, "Summary on high-level artificial general intelligence"])
#     # pytest.fail("TODO")