from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

import yaml

from libreprimus.token_block.stage5dg import DATA_PATHS, SCHEMA_PATHS, build_stage5dg

ROOT = Path(__file__).resolve().parents[2]
STAGE5DG_RECORDS = [path.as_posix() for path in DATA_PATHS.values()]
STAGE5DG_SCHEMAS = list(SCHEMA_PATHS.values())
SELECTED_OPTION_ID = "prepare_real_operator_approval_record"


def ensure_stage5dg_built() -> None:
    if all((ROOT / path).exists() for path in STAGE5DG_RECORDS + STAGE5DG_SCHEMAS):
        return
    build_stage5dg()


def load_yaml(path: str | Path) -> dict[str, Any]:
    return yaml.safe_load((ROOT / path).read_text(encoding="utf-8")) or {}


def git_check_ignore(path: str) -> bool:
    result = subprocess.run(["git", "check-ignore", "-q", path], cwd=ROOT, check=False)
    return result.returncode == 0
