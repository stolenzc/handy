import json
from pathlib import Path

_DEFAULT_CONFIG = Path.home() / ".config" / "handy" / "config.json"


def load_config(path: Path | None = None) -> dict:
    """Load config, falling back to defaults for missing keys."""
    path = path or _DEFAULT_CONFIG
    config = {}
    if path.is_file():
        with open(path) as f:
            config.update(json.load(f))
    return config
