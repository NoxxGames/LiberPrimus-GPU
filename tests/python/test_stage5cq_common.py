import subprocess
from pathlib import Path
from typing import Any

import yaml

from libreprimus.token_block.stage5cq import DATA_PATHS, SCHEMA_PATHS, build_stage5cq

ROOT = Path(__file__).resolve().parents[2]
STAGE5CQ_RECORDS = [path.as_posix() for path in DATA_PATHS.values()]
STAGE5CQ_SCHEMAS = list(SCHEMA_PATHS.values())


def ensure_stage5cq_built() -> None:
    build_stage5cq()


def load_yaml(path: str | Path) -> dict[str, Any]:
    return yaml.safe_load((ROOT / path).read_text(encoding="utf-8")) or {}


def git_check_ignore(path: str) -> bool:
    result = subprocess.run(["git", "check-ignore", "-q", path], cwd=ROOT, check=False)
    return result.returncode == 0
