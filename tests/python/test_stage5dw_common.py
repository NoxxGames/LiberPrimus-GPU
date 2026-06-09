from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

from libreprimus.token_block.stage5dw import DATA_PATHS, SCHEMA_PATHS, build_stage5dw

ROOT = Path(__file__).resolve().parents[2]
STAGE5DW_RECORDS = [path.as_posix() for path in DATA_PATHS.values()]
STAGE5DW_SCHEMAS = [path.as_posix() for path in SCHEMA_PATHS.values()]
_STAGE5DW_BUILT = False


def ensure_stage5dw_built() -> None:
    global _STAGE5DW_BUILT
    if _STAGE5DW_BUILT:
        return
    if all((ROOT / path).exists() for path in STAGE5DW_RECORDS + STAGE5DW_SCHEMAS):
        _STAGE5DW_BUILT = True
        return
    build_stage5dw()
    _STAGE5DW_BUILT = True


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
