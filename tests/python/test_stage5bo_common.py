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


STAGE5BO_RECORDS = [
    "data/token-block/stage5bo-decision-template-correction-source-lock.yaml",
    "data/token-block/stage5bo-token-case-human-review-errata.yaml",
    "data/token-block/stage5bo-token-case-correction-impact-summary.yaml",
    "data/token-block/stage5bo-errata-aware-token-option-universe.yaml",
    "data/token-block/stage5bo-string4-branch-membership-after-errata.yaml",
    "data/token-block/stage5bo-stage5bn-addendum-integration.yaml",
    "data/token-block/stage5bo-string4-source-gap-closure-after-errata.yaml",
    "data/token-block/stage5bo-string4-planning-constraint-update.yaml",
    "data/token-block/stage5bo-token-block-lineage-preservation.yaml",
    "data/token-block/stage5bo-future-dry-run-planning-impact.yaml",
    "data/historical-route/stage5bo-source-gap-severity-update.yaml",
    "data/historical-route/stage5bo-dwh-quarantine-reaffirmation.yaml",
    "data/historical-route/stage5bo-guardrail.yaml",
    "data/source-harvester/stage5bo-codex-handoff-policy.yaml",
    "data/project-state/stage5bo-summary.yaml",
    "data/project-state/stage5bo-next-stage-decision.yaml",
]
