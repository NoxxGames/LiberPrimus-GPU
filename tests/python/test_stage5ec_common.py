from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

from libreprimus.token_block.stage5ec import DATA_PATHS, SCHEMA_PATHS, build_stage5ec

ROOT = Path(__file__).resolve().parents[2]
STAGE5EC_RECORDS = [path.as_posix() for path in DATA_PATHS.values()]
STAGE5EC_SCHEMAS = [path.as_posix() for path in SCHEMA_PATHS.values()]
_STAGE5EC_BUILT = False


def ensure_stage5ec_built() -> None:
    global _STAGE5EC_BUILT
    if _STAGE5EC_BUILT:
        return
    if all((ROOT / path).exists() for path in STAGE5EC_RECORDS + STAGE5EC_SCHEMAS):
        _STAGE5EC_BUILT = True
        return
    build_stage5ec()
    _STAGE5EC_BUILT = True


def load_yaml(path: str | Path) -> dict[str, Any]:
    return yaml.safe_load((ROOT / path).read_text(encoding="utf-8")) or {}


def run_token_block_cli(*args: str) -> str:
    result = subprocess.run(
        [sys.executable, "-m", "libreprimus.cli", "token-block", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout
