from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

import yaml

from libreprimus.token_block.stage5dk import DATA_PATHS, SCHEMA_PATHS, build_stage5dk

ROOT = Path(__file__).resolve().parents[2]
STAGE5DK_RECORDS = [path.as_posix() for path in DATA_PATHS.values()]
STAGE5DK_SCHEMAS = [path.as_posix() for path in SCHEMA_PATHS.values()]
_STAGE5DK_BUILT = False


def ensure_stage5dk_built() -> None:
    global _STAGE5DK_BUILT
    if _STAGE5DK_BUILT:
        return
    if all((ROOT / path).exists() for path in STAGE5DK_RECORDS + STAGE5DK_SCHEMAS):
        _STAGE5DK_BUILT = True
        return
    build_stage5dk(fetch_web=False)
    _STAGE5DK_BUILT = True


def load_yaml(path: str | Path) -> dict[str, Any]:
    return yaml.safe_load((ROOT / path).read_text(encoding="utf-8")) or {}


def write_temp_yaml(path: Path, payload: dict[str, Any]) -> Path:
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
    return path


def git_check_ignore(path: str) -> bool:
    result = subprocess.run(["git", "check-ignore", "-q", path], cwd=ROOT, check=False)
    return result.returncode == 0
