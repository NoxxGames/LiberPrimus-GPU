from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

import yaml

from libreprimus.token_block.stage5cw import DATA_PATHS, SCHEMA_PATHS, build_stage5cw

ROOT = Path(__file__).resolve().parents[2]
STAGE5CW_RECORDS = [path.as_posix() for path in DATA_PATHS.values()]
STAGE5CW_SCHEMAS = list(SCHEMA_PATHS.values())
_STAGE5CW_BUILT = False


def ensure_stage5cw_built() -> None:
    global _STAGE5CW_BUILT
    if _STAGE5CW_BUILT:
        return
    if all((ROOT / path).exists() for path in STAGE5CW_RECORDS + STAGE5CW_SCHEMAS):
        _STAGE5CW_BUILT = True
        return
    build_stage5cw()
    _STAGE5CW_BUILT = True


def load_yaml(path: str | Path) -> dict[str, Any]:
    return yaml.safe_load((ROOT / path).read_text(encoding="utf-8")) or {}


def git_check_ignore(path: str) -> bool:
    result = subprocess.run(["git", "check-ignore", "-q", path], cwd=ROOT, check=False)
    return result.returncode == 0
