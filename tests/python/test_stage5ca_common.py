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


STAGE5CA_RECORDS = [
    "data/project-state/stage5ca-summary.yaml",
    "data/project-state/stage5ca-next-stage-decision.yaml",
    "data/project-state/stage5ca-stage5bz-findings-integration.yaml",
    "data/project-state/stage5ca-reviewable-stage-marker.yaml",
    "data/project-state/stage5ca-reviewable-validation-evidence.yaml",
    "data/project-state/stage5ca-reviewable-source-digest-index.yaml",
    "data/project-state/stage5ca-reviewability-gap-register.yaml",
    "data/project-state/stage5ca-record-family-name-equivalence-map.yaml",
    "data/token-block/stage5ca-inactive-sidecar-review-contract.yaml",
    "data/token-block/stage5ca-future-runner-exact-citation-contract.yaml",
    "data/token-block/stage5ca-future-runner-citation-validation-requirements.yaml",
    "data/token-block/stage5ca-fail-closed-trigger-contract.yaml",
    "data/token-block/stage5ca-fail-closed-trigger-validation-requirements.yaml",
    "data/token-block/stage5ca-activation-precondition-contract.yaml",
    "data/token-block/stage5ca-activation-precondition-validation-requirements.yaml",
    "data/token-block/stage5ca-manifest-supersession-preflight-contract.yaml",
    "data/token-block/stage5ca-manifest-supersession-review-determinism.yaml",
    "data/token-block/stage5ca-sidecar-to-active-transition-policy.yaml",
    "data/token-block/stage5ca-sidecar-activation-blocker.yaml",
    "data/token-block/stage5ca-stage5by-sidecar-scaffold-preservation.yaml",
    "data/token-block/stage5ca-stage5bd-plan-preservation.yaml",
    "data/token-block/stage5ca-active-lineage-preservation.yaml",
    "data/token-block/stage5ca-no-active-ingestion-proof.yaml",
    "data/token-block/stage5ca-no-byte-stream-proof.yaml",
    "data/token-block/stage5ca-future-dry-run-planning-impact.yaml",
    "data/historical-route/stage5ca-source-gap-severity-update.yaml",
    "data/historical-route/stage5ca-dwh-quarantine-reaffirmation.yaml",
    "data/historical-route/stage5ca-guardrail.yaml",
    "data/source-harvester/stage5ca-codex-handoff-policy.yaml",
    "data/source-harvester/stage5ca-review-packaging-warning.yaml",
]
