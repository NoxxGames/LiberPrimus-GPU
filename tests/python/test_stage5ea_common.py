from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

from libreprimus.token_block.stage5ea import DATA_PATHS, SCHEMA_PATHS, build_stage5ea

ROOT = Path(__file__).resolve().parents[2]
_BUILT = False


def ensure_stage5ea_built() -> None:
    global _BUILT
    if _BUILT:
        return
    if all((ROOT / path).exists() for path in [*DATA_PATHS.values(), *SCHEMA_PATHS.values()]):
        _BUILT = True
        return
    build_stage5ea()
    _BUILT = True


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
