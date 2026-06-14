from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from libreprimus.token_block import stage6


def load_yaml(path: str | Path) -> Any:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def stage6_data(key: str) -> Any:
    path = stage6.DATA_PATHS[key]
    if not path.exists():
        stage6.build_stage6()
    return load_yaml(path)
