from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

import yaml

from libreprimus.token_block.stage5dr import DATA_PATHS, SCHEMA_PATHS, build_stage5dr

ROOT = Path(__file__).resolve().parents[2]
STAGE5DR_RECORDS = [path.as_posix() for path in DATA_PATHS.values()]
STAGE5DR_SCHEMAS = [path.as_posix() for path in SCHEMA_PATHS.values()]
_STAGE5DR_BUILT = False


def ensure_stage5dr_built() -> None:
    global _STAGE5DR_BUILT
    if _STAGE5DR_BUILT:
        return
    if all((ROOT / path).exists() for path in STAGE5DR_RECORDS + STAGE5DR_SCHEMAS):
        _STAGE5DR_BUILT = True
        return
    build_stage5dr()
    _STAGE5DR_BUILT = True


def load_yaml(path: str | Path) -> dict[str, Any]:
    return yaml.safe_load((ROOT / path).read_text(encoding="utf-8")) or {}


def git_check_ignore(path: str) -> bool:
    result = subprocess.run(["git", "check-ignore", "-q", path], cwd=ROOT, check=False)
    return result.returncode == 0
