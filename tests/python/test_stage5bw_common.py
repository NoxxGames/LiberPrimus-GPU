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


STAGE5BW_RECORDS = [
    "data/project-state/stage5bw-stage5bv-findings-integration.yaml",
    "data/project-state/stage5bw-reviewable-stage-marker.yaml",
    "data/project-state/stage5bw-reviewable-validation-evidence.yaml",
    "data/project-state/stage5bw-reviewable-source-digest-index.yaml",
    "data/project-state/stage5bw-reviewability-gap-register.yaml",
    "data/project-state/stage5bw-summary.yaml",
    "data/project-state/stage5bw-next-stage-decision.yaml",
    "data/token-block/stage5bw-inactive-sidecar-planning-ingestion-proposal.yaml",
    "data/token-block/stage5bw-inactive-sidecar-consumption-model.yaml",
    "data/token-block/stage5bw-manifest-supersession-preflight.yaml",
    "data/token-block/stage5bw-manifest-validation-preflight.yaml",
    "data/token-block/stage5bw-active-lineage-preservation.yaml",
    "data/token-block/stage5bw-preserved-active-lineage-digest-index.yaml",
    "data/token-block/stage5bw-stage5bd-plan-preservation.yaml",
    "data/token-block/stage5bw-future-runner-citation-requirements.yaml",
    "data/token-block/stage5bw-active-ingestion-blocker-preservation.yaml",
    "data/token-block/stage5bw-no-byte-stream-gate.yaml",
    "data/token-block/stage5bw-no-active-ingestion-proof.yaml",
    "data/token-block/stage5bw-string4-gate-preservation.yaml",
    "data/token-block/stage5bw-future-dry-run-planning-impact.yaml",
    "data/token-block/stage5bw-gate-readiness-matrix.yaml",
    "data/token-block/stage5bw-future-stage-authorization-policy.yaml",
    "data/historical-route/stage5bw-source-gap-severity-update.yaml",
    "data/historical-route/stage5bw-dwh-quarantine-reaffirmation.yaml",
    "data/historical-route/stage5bw-guardrail.yaml",
    "data/source-harvester/stage5bw-review-packaging-warning.yaml",
    "data/source-harvester/stage5bw-codex-handoff-policy.yaml",
]
