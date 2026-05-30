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


STAGE5CE_RECORDS = [
    "data/project-state/stage5ce-summary.yaml",
    "data/project-state/stage5ce-next-stage-decision.yaml",
    "data/project-state/stage5ce-stage5cd-findings-integration.yaml",
    "data/project-state/stage5ce-reviewable-stage-marker.yaml",
    "data/project-state/stage5ce-reviewable-validation-evidence.yaml",
    "data/project-state/stage5ce-reviewable-source-digest-index.yaml",
    "data/project-state/stage5ce-reviewability-gap-register.yaml",
    "data/project-state/stage5ce-record-family-name-equivalence-map.yaml",
    "data/token-block/stage5ce-active-planning-input-proposal-package.yaml",
    "data/token-block/stage5ce-proposal-package-citation-set.yaml",
    "data/token-block/stage5ce-operator-approval-gate-design.yaml",
    "data/token-block/stage5ce-deep-research-approval-gate-design.yaml",
    "data/token-block/stage5ce-operator-deep-research-combined-gate-contract.yaml",
    "data/token-block/stage5ce-approval-gate-validation-requirements.yaml",
    "data/token-block/stage5ce-stage5cc-contract-preservation.yaml",
    "data/token-block/stage5ce-stage5cc-citation-negative-test-hardening.yaml",
    "data/token-block/stage5ce-committed-pytest-count-capture.yaml",
    "data/token-block/stage5ce-active-planning-input-nonactivation-proof.yaml",
    "data/token-block/stage5ce-no-active-ingestion-proof.yaml",
    "data/token-block/stage5ce-no-byte-stream-transition-gate.yaml",
    "data/token-block/stage5ce-no-execution-transition-gate.yaml",
    "data/token-block/stage5ce-manifest-supersession-nonactivation-proof.yaml",
    "data/token-block/stage5ce-stage5bd-plan-preservation.yaml",
    "data/token-block/stage5ce-active-lineage-preservation.yaml",
    "data/token-block/stage5ce-sidecar-activation-blocker.yaml",
    "data/token-block/stage5ce-future-dry-run-planning-impact.yaml",
    "data/token-block/stage5ce-sidecar-to-active-transition-package-policy.yaml",
    "data/historical-route/stage5ce-dwh-quarantine-reaffirmation.yaml",
    "data/historical-route/stage5ce-source-gap-severity-update.yaml",
    "data/historical-route/stage5ce-guardrail.yaml",
    "data/source-harvester/stage5ce-codex-handoff-policy.yaml",
    "data/source-harvester/stage5ce-review-packaging-warning.yaml",
]
