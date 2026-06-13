from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from libreprimus.token_block import stage5ei


def load_yaml(path: str | Path) -> Any:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def stage5ei_data(key: str) -> Any:
    path = stage5ei.DATA_PATHS[key]
    if not path.exists():
        stage5ei.build_stage5ei()
    return load_yaml(path)

