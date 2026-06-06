from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

import yaml

from libreprimus.token_block.stage5dl import DATA_PATHS, SCHEMA_PATHS, build_stage5dl

ROOT = Path(__file__).resolve().parents[2]
STAGE5DL_RECORDS = [path.as_posix() for path in DATA_PATHS.values()]
STAGE5DL_SCHEMAS = [path.as_posix() for path in SCHEMA_PATHS.values()]
_STAGE5DL_BUILT = False


def ensure_stage5dl_built() -> None:
    global _STAGE5DL_BUILT
    if _STAGE5DL_BUILT:
        return
    if all((ROOT / path).exists() for path in STAGE5DL_RECORDS + STAGE5DL_SCHEMAS):
        _STAGE5DL_BUILT = True
        return
    build_stage5dl(write_completion=False)
    _STAGE5DL_BUILT = True


def load_yaml(path: str | Path) -> dict[str, Any]:
    return yaml.safe_load((ROOT / path).read_text(encoding="utf-8")) or {}


def write_temp_yaml(path: Path, payload: dict[str, Any]) -> Path:
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
    return path


def git_check_ignore(path: str) -> bool:
    result = subprocess.run(["git", "check-ignore", "-q", path], cwd=ROOT, check=False)
    return result.returncode == 0
