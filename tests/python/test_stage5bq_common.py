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


STAGE5BQ_RECORDS = [
    "data/project-state/stage5bq-stage5bp-findings-integration.yaml",
    "data/source-harvester/stage5bq-review-packaging-warning.yaml",
    "data/token-block/stage5bq-string4-inactive-branch-planning-context.yaml",
    "data/token-block/stage5bq-operator-errata-sidecar-status.yaml",
    "data/token-block/stage5bq-errata-aware-dry-run-constraint-update.yaml",
    "data/token-block/stage5bq-string4-no-active-ingestion-proof.yaml",
    "data/token-block/stage5bq-future-dry-run-requirements.yaml",
    "data/token-block/stage5bq-active-manifest-preservation.yaml",
    "data/token-block/stage5bq-stage5bd-dry-run-lineage-preservation.yaml",
    "data/token-block/stage5bq-future-dry-run-planning-impact.yaml",
    "data/historical-route/stage5bq-source-gap-severity-update.yaml",
    "data/historical-route/stage5bq-dwh-quarantine-reaffirmation.yaml",
    "data/historical-route/stage5bq-guardrail.yaml",
    "data/source-harvester/stage5bq-codex-handoff-policy.yaml",
    "data/project-state/stage5bq-summary.yaml",
    "data/project-state/stage5bq-next-stage-decision.yaml",
]
