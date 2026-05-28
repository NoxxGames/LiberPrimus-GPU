import json
import subprocess
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]


def load_yaml(path: str) -> dict[str, Any]:
    return yaml.safe_load((ROOT / path).read_text(encoding="utf-8")) or {}


def load_json(path: str) -> dict[str, Any]:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def run_git_check_ignore(path: str) -> bool:
    result = subprocess.run(["git", "check-ignore", "-q", path], cwd=ROOT, check=False)
    return result.returncode == 0


STAGE5BN_RECORDS = [
    "data/token-block/stage5bn-string4-unsupported-position-target.yaml",
    "data/token-block/stage5bn-string4-unsupported-position-source-evidence.yaml",
    "data/token-block/stage5bn-stage5aw-option-gap-audit.yaml",
    "data/token-block/stage5bn-local-spreadsheet-target-cell-audit.yaml",
    "data/token-block/stage5bn-target-position-coordinate-context.yaml",
    "data/token-block/stage5bn-human-review-pack-manifest.yaml",
    "data/token-block/stage5bn-proposed-token-option-addendum.yaml",
    "data/token-block/stage5bn-string4-source-gap-closure-status.yaml",
    "data/token-block/stage5bn-string4-planning-constraint-update.yaml",
    "data/token-block/stage5bn-token-block-lineage-preservation.yaml",
    "data/historical-route/stage5bn-source-gap-severity-update.yaml",
    "data/historical-route/stage5bn-dwh-quarantine-reaffirmation.yaml",
    "data/historical-route/stage5bn-guardrail.yaml",
    "data/source-harvester/stage5bn-codex-handoff-policy.yaml",
    "data/project-state/stage5bn-summary.yaml",
    "data/project-state/stage5bn-next-stage-decision.yaml",
]
