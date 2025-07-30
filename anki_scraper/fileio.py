from pathlib import Path
import toml

from appdirs import user_config_dir

CONFIG_DIR  = Path(user_config_dir("anki-scraper"))
CONFIG_FILE = CONFIG_DIR / "config.toml"

def save_output_dir(new_dir: Path):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        toml.dump({"output_dir": str(new_dir)}, f)

def load_output_dir():
    if not CONFIG_FILE.exists():
        return Path.cwd()
    cfg = toml.loads(CONFIG_FILE.read_text())
    return Path(cfg.get("output_dir", "."))