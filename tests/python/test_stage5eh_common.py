from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from libreprimus.token_block import stage5eh


def load_yaml(path: str | Path) -> Any:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def stage5eh_data(key: str) -> Any:
    path = stage5eh.DATA_PATHS[key]
    if not path.exists():
        stage5eh.build_stage5eh()
    return load_yaml(path)
