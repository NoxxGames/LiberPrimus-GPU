from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from libreprimus.token_block import stage5ef

_BUILT = False


def ensure_stage5ef_built() -> None:
    global _BUILT
    if not _BUILT:
        stage5ef.build_stage5ef()
        _BUILT = True


def load_yaml(path: str | Path) -> Any:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def stage5ef_data(key: str) -> Any:
    ensure_stage5ef_built()
    return load_yaml(stage5ef.DATA_PATHS[key])
