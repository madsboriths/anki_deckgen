import os, sys

from openai import OpenAI
from .adapters.telegram_adapter import TelegramAdapter
from .adapters.cli_adapter import typer_cli_app
from .adapters.openai_adapter import OpenAIAdapter
from .adapters.anki_adapter import AnkiFlashcardAdapter
from .core.service import Service

def run_bot():
    openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    flashcard_client = AnkiFlashcardAdapter()
    service = Service(llm_client=OpenAIAdapter(openai_client, model="gpt-5-nano"), flashcard_client=flashcard_client)
    TelegramAdapter(os.environ["TELEGRAM_BOT_TOKEN"]).start(on_message=service.handle_user_request)

def run_cli():
    typer_cli_app()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "bot":
        print("Running bot...")
        run_bot()
    else:
        print("Running cli...")
        run_cli()