from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

from libreprimus.token_block.stage5ee import DATA_PATHS, SCHEMA_PATHS, build_stage5ee

ROOT = Path(__file__).resolve().parents[2]
stage5ee_RECORDS = [path.as_posix() for path in DATA_PATHS.values()]
stage5ee_SCHEMAS = [path.as_posix() for path in SCHEMA_PATHS.values()]
_stage5ee_BUILT = False


def ensure_stage5ee_built() -> None:
    global _stage5ee_BUILT
    if _stage5ee_BUILT:
        return
    if all((ROOT / path).exists() for path in stage5ee_RECORDS + stage5ee_SCHEMAS):
        _stage5ee_BUILT = True
        return
    build_stage5ee()
    _stage5ee_BUILT = True


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
