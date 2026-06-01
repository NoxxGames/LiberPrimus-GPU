import subprocess
from pathlib import Path
from typing import Any

import yaml

from libreprimus.token_block.stage5co import DATA_PATHS, SCHEMA_PATHS

ROOT = Path(__file__).resolve().parents[2]
STAGE5CO_RECORDS = [path.as_posix() for path in DATA_PATHS.values()]
STAGE5CO_SCHEMAS = list(SCHEMA_PATHS.values())


def load_yaml(path: str | Path) -> dict[str, Any]:
    return yaml.safe_load((ROOT / path).read_text(encoding="utf-8")) or {}


def git_check_ignore(path: str) -> bool:
    result = subprocess.run(["git", "check-ignore", "-q", path], cwd=ROOT, check=False)
    return result.returncode == 0
