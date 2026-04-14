import toml
import os
from pathlib import Path

CONFIG_DIR = Path.home() / ".envsync"
CONFIG_FILE = CONFIG_DIR / "config.toml"

def init_config(project_id: str, service_account_path: str):
    CONFIG_DIR.mkdir(exist_ok=True)
    config = {
        "settings": {
            "project_id": project_id,
            "service_account_path": service_account_path
        }
    }
    with open(CONFIG_FILE, "w") as f:
        toml.dump(config, f)

def load_config() -> dict:
    with open(CONFIG_FILE, "r") as f:
        return toml.load(f)["settings"]

def config_exists() -> bool:
    return CONFIG_FILE.exists()