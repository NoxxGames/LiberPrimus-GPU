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


STAGE5CC_RECORDS = [
    "data/project-state/stage5cc-summary.yaml",
    "data/project-state/stage5cc-next-stage-decision.yaml",
    "data/project-state/stage5cc-stage5cb-findings-integration.yaml",
    "data/project-state/stage5cc-reviewable-stage-marker.yaml",
    "data/project-state/stage5cc-reviewable-validation-evidence.yaml",
    "data/project-state/stage5cc-reviewable-source-digest-index.yaml",
    "data/project-state/stage5cc-reviewability-gap-register.yaml",
    "data/project-state/stage5cc-record-family-name-equivalence-map.yaml",
    "data/token-block/stage5cc-stage5ca-contract-preservation.yaml",
    "data/token-block/stage5cc-fail-closed-trigger-exact-set-contract.yaml",
    "data/token-block/stage5cc-fail-closed-trigger-extension-policy.yaml",
    "data/token-block/stage5cc-fail-closed-trigger-validation-requirements.yaml",
    "data/token-block/stage5cc-activation-precondition-exact-set-contract.yaml",
    "data/token-block/stage5cc-activation-precondition-extension-policy.yaml",
    "data/token-block/stage5cc-activation-precondition-validation-requirements.yaml",
    "data/token-block/stage5cc-active-planning-input-proposal-preflight.yaml",
    "data/token-block/stage5cc-sidecar-to-active-transition-preflight.yaml",
    "data/token-block/stage5cc-no-byte-stream-transition-gate.yaml",
    "data/token-block/stage5cc-no-execution-transition-gate.yaml",
    "data/token-block/stage5cc-manifest-supersession-nonactivation-proof.yaml",
    "data/token-block/stage5cc-stage5bd-plan-preservation.yaml",
    "data/token-block/stage5cc-active-lineage-preservation.yaml",
    "data/token-block/stage5cc-no-active-ingestion-proof.yaml",
    "data/token-block/stage5cc-no-byte-stream-proof.yaml",
    "data/token-block/stage5cc-future-runner-citation-contract-preservation.yaml",
    "data/token-block/stage5cc-sidecar-activation-blocker.yaml",
    "data/token-block/stage5cc-future-dry-run-planning-impact.yaml",
    "data/historical-route/stage5cc-dwh-quarantine-reaffirmation.yaml",
    "data/historical-route/stage5cc-source-gap-severity-update.yaml",
    "data/historical-route/stage5cc-guardrail.yaml",
    "data/source-harvester/stage5cc-codex-handoff-policy.yaml",
    "data/source-harvester/stage5cc-review-packaging-warning.yaml",
]
