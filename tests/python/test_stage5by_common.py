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


def git_check_ignore(path: str) -> bool:
    result = subprocess.run(["git", "check-ignore", "-q", path], cwd=ROOT, check=False)
    return result.returncode == 0


STAGE5BY_RECORDS = [
    "data/project-state/stage5by-stage5bx-findings-integration.yaml",
    "data/project-state/stage5by-stage5bw-source-digest-duplicate-review.yaml",
    "data/project-state/stage5by-record-family-name-equivalence-map.yaml",
    "data/project-state/stage5by-reviewable-stage-marker.yaml",
    "data/project-state/stage5by-reviewable-validation-evidence.yaml",
    "data/project-state/stage5by-reviewable-source-digest-index.yaml",
    "data/project-state/stage5by-reviewability-gap-register.yaml",
    "data/project-state/stage5by-summary.yaml",
    "data/project-state/stage5by-next-stage-decision.yaml",
    "data/token-block/stage5by-inactive-sidecar-planning-manifest-scaffold.yaml",
    "data/token-block/stage5by-no-execution-planning-ingestion-sidecar.yaml",
    "data/token-block/stage5by-sidecar-activation-blocker.yaml",
    "data/token-block/stage5by-no-active-ingestion-proof.yaml",
    "data/token-block/stage5by-no-byte-stream-proof.yaml",
    "data/token-block/stage5by-manifest-supersession-readiness-preflight.yaml",
    "data/token-block/stage5by-stage5bd-plan-preservation.yaml",
    "data/token-block/stage5by-active-lineage-preservation.yaml",
    "data/token-block/stage5by-future-runner-citation-requirements.yaml",
    "data/token-block/stage5by-sidecar-planning-manifest-validation-requirements.yaml",
    "data/token-block/stage5by-future-dry-run-planning-impact.yaml",
    "data/historical-route/stage5by-dwh-quarantine-reaffirmation.yaml",
    "data/historical-route/stage5by-source-gap-severity-update.yaml",
    "data/historical-route/stage5by-guardrail.yaml",
    "data/source-harvester/stage5by-codex-handoff-policy.yaml",
    "data/source-harvester/stage5by-review-packaging-warning.yaml",
]
