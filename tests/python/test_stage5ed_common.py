from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

from libreprimus.token_block.stage5ed import DATA_PATHS, SCHEMA_PATHS, build_stage5ed

ROOT = Path(__file__).resolve().parents[2]
STAGE5ED_RECORDS = [path.as_posix() for path in DATA_PATHS.values()]
STAGE5ED_SCHEMAS = [path.as_posix() for path in SCHEMA_PATHS.values()]
_STAGE5ED_BUILT = False


def ensure_stage5ed_built() -> None:
    global _STAGE5ED_BUILT
    if _STAGE5ED_BUILT:
        return
    if all((ROOT / path).exists() for path in STAGE5ED_RECORDS + STAGE5ED_SCHEMAS):
        _STAGE5ED_BUILT = True
        return
    build_stage5ed()
    _STAGE5ED_BUILT = True


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
