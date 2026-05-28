import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]


def load_yaml(path: str) -> dict[str, Any]:
    return yaml.safe_load((ROOT / path).read_text(encoding="utf-8")) or {}


def load_json(path: str) -> dict[str, Any]:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def run_git_check_ignore(path: str) -> bool:
    import subprocess

    result = subprocess.run(["git", "check-ignore", "-q", path], cwd=ROOT, check=False)
    return result.returncode == 0


STAGE5BM_RECORDS = [
    "data/project-state/stage5bm-stage5bl-findings-integration.yaml",
    "data/source-harvester/stage5bm-review-packaging-warning.yaml",
    "data/token-block/stage5bm-string4-source-restatement.yaml",
    "data/token-block/stage5bm-string4-primary60-inverse-policy.yaml",
    "data/token-block/stage5bm-string4-stage5ap-mismatch-analysis.yaml",
    "data/token-block/stage5bm-string4-stage5aw-branch-membership.yaml",
    "data/token-block/stage5bm-string4-ambiguity-class-coverage.yaml",
    "data/token-block/stage5bm-string4-planning-constraint.yaml",
    "data/token-block/stage5bm-token-block-lineage-preservation.yaml",
    "data/token-block/stage5bm-future-dry-run-planning-impact.yaml",
    "data/historical-route/stage5bm-source-gap-severity-update.yaml",
    "data/historical-route/stage5bm-historical-family-granularity-update.yaml",
    "data/historical-route/stage5bm-dwh-quarantine-reaffirmation.yaml",
    "data/historical-route/stage5bm-stage5bj-errata-supersession.yaml",
    "data/historical-route/stage5bm-guardrail.yaml",
    "data/source-harvester/stage5bm-codex-handoff-policy.yaml",
    "data/project-state/stage5bm-summary.yaml",
    "data/project-state/stage5bm-next-stage-decision.yaml",
]
