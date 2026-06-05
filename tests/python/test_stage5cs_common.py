import subprocess
from pathlib import Path
from typing import Any

import yaml

from libreprimus.token_block.stage5cs import DATA_PATHS, SCHEMA_PATHS, build_stage5cs

ROOT = Path(__file__).resolve().parents[2]
STAGE5CS_RECORDS = [path.as_posix() for path in DATA_PATHS.values()]
STAGE5CS_SCHEMAS = list(SCHEMA_PATHS.values())
_STAGE5CS_BUILT = False


def ensure_stage5cs_built() -> None:
    global _STAGE5CS_BUILT
    if _STAGE5CS_BUILT:
        return
    if all((ROOT / path).exists() for path in STAGE5CS_RECORDS + STAGE5CS_SCHEMAS):
        _STAGE5CS_BUILT = True
        return
    build_stage5cs()
    _STAGE5CS_BUILT = True


def load_yaml(path: str | Path) -> dict[str, Any]:
    return yaml.safe_load((ROOT / path).read_text(encoding="utf-8")) or {}


def git_check_ignore(path: str) -> bool:
    result = subprocess.run(["git", "check-ignore", "-q", path], cwd=ROOT, check=False)
    return result.returncode == 0
