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


STAGE5BU_RECORDS = [
    "data/project-state/stage5bu-stage5bt-findings-integration.yaml",
    "data/project-state/stage5bu-reviewable-stage-marker.yaml",
    "data/project-state/stage5bu-reviewable-validation-evidence.yaml",
    "data/project-state/stage5bu-reviewable-source-digest-index.yaml",
    "data/project-state/stage5bu-reviewability-gap-register.yaml",
    "data/token-block/stage5bu-stage5bs-lineage-path-erratum.yaml",
    "data/token-block/stage5bu-active-manifest-preservation-repair.yaml",
    "data/token-block/stage5bu-preserved-active-lineage-digest-index.yaml",
    "data/token-block/stage5bu-lineage-path-resolution-validation.yaml",
    "data/token-block/stage5bu-stage5bs-validator-hardening.yaml",
    "data/token-block/stage5bu-future-runner-citation-policy-repair.yaml",
    "data/token-block/stage5bu-string4-gate-preservation.yaml",
    "data/token-block/stage5bu-no-active-ingestion-proof.yaml",
    "data/token-block/stage5bu-stage5bd-plan-preservation.yaml",
    "data/token-block/stage5bu-future-dry-run-planning-impact.yaml",
    "data/historical-route/stage5bu-source-gap-severity-update.yaml",
    "data/historical-route/stage5bu-dwh-quarantine-reaffirmation.yaml",
    "data/historical-route/stage5bu-guardrail.yaml",
    "data/source-harvester/stage5bu-codex-handoff-policy.yaml",
    "data/source-harvester/stage5bu-review-packaging-warning.yaml",
    "data/project-state/stage5bu-summary.yaml",
    "data/project-state/stage5bu-next-stage-decision.yaml",
]
