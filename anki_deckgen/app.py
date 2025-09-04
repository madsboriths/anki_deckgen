import os, sys
from .adapters.telegram_adapter import TelegramAdapter
from .adapters.cli_adapter import typer_cli_app
from .core.service import handle_user_request

def run_bot():
    TelegramAdapter(os.environ["TELEGRAM_BOT_TOKEN"]).start(on_message=handle_user_request)

def run_cli():
    typer_cli_app()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "bot":
        run_bot()
    else:
        run_cli()