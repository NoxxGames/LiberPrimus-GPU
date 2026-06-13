from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from libreprimus.token_block import stage5eg

_BUILT = False


def ensure_stage5eg_built() -> None:
    global _BUILT
    if not _BUILT:
        successor_present = Path("data/project-state/stage5eh-summary.yaml").exists()
        stage5eg_records_present = all(path.exists() for path in stage5eg.DATA_PATHS.values())
        if not (successor_present and stage5eg_records_present):
            stage5eg.build_stage5eg()
        _BUILT = True


def load_yaml(path: str | Path) -> Any:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def stage5eg_data(key: str) -> Any:
    ensure_stage5eg_built()
    return load_yaml(stage5eg.DATA_PATHS[key])
