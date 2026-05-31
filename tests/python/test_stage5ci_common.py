import subprocess
from pathlib import Path
from typing import Any

import yaml

from libreprimus.token_block.stage5ci import DATA_PATHS

ROOT = Path(__file__).resolve().parents[2]
STAGE5CI_RECORDS = [path.as_posix() for path in DATA_PATHS.values()]


def load_yaml(path: str) -> dict[str, Any]:
    return yaml.safe_load((ROOT / path).read_text(encoding="utf-8")) or {}


def write_yaml(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(yaml.safe_dump(payload, sort_keys=True), encoding="utf-8")


def git_check_ignore(path: str) -> bool:
    result = subprocess.run(["git", "check-ignore", "-q", path], cwd=ROOT, check=False)
    return result.returncode == 0
