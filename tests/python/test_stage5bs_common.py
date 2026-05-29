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


STAGE5BS_RECORDS = [
    "data/project-state/stage5bs-stage5br-findings-integration.yaml",
    "data/project-state/stage5bs-reviewable-stage-marker.yaml",
    "data/project-state/stage5bs-reviewable-validation-evidence.yaml",
    "data/project-state/stage5bs-reviewable-source-digest-index.yaml",
    "data/project-state/stage5bs-reviewability-gap-register.yaml",
    "data/source-harvester/stage5bs-review-packaging-warning.yaml",
    "data/token-block/stage5bs-string4-planning-ingestion-gate.yaml",
    "data/token-block/stage5bs-future-runner-citation-policy.yaml",
    "data/token-block/stage5bs-inactive-sidecar-consumption-policy.yaml",
    "data/token-block/stage5bs-active-ingestion-blocker.yaml",
    "data/token-block/stage5bs-no-active-ingestion-proof.yaml",
    "data/token-block/stage5bs-string4-gate-readiness-matrix.yaml",
    "data/token-block/stage5bs-manifest-validation-requirements.yaml",
    "data/token-block/stage5bs-future-stage-authorization-policy.yaml",
    "data/token-block/stage5bs-stage5bd-plan-preservation.yaml",
    "data/token-block/stage5bs-active-manifest-preservation.yaml",
    "data/token-block/stage5bs-future-dry-run-planning-impact.yaml",
    "data/historical-route/stage5bs-source-gap-severity-update.yaml",
    "data/historical-route/stage5bs-dwh-quarantine-reaffirmation.yaml",
    "data/historical-route/stage5bs-guardrail.yaml",
    "data/source-harvester/stage5bs-codex-handoff-policy.yaml",
    "data/project-state/stage5bs-summary.yaml",
    "data/project-state/stage5bs-next-stage-decision.yaml",
]
