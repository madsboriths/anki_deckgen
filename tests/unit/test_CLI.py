import pytest
from typer.testing import CliRunner
from anki_scraper.cli import app 

runner = CliRunner()

def test_hello_without_args():
    result = runner.invoke(app, ["hello"])
    assert result.exit_code == 0
    assert result.stdout.strip() == "Hello world!"