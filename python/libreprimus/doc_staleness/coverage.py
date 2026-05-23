"""Operational-file-map coverage checks."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

REQUIRED_PATHS = (
    "README.md",
    "STATUS.md",
    "ROADMAP.md",
    "AGENTS.md",
    "CUDA_NOTES.md",
    "BENCHMARKS.md",
    "EXPERIMENTS.md",
    "RESULTS_SCHEMA.md",
    "TESTING.md",
    "CIPHER_CATALOG.md",
    "docs/roadmap/staged-plan.md",
    "docs/onboarding/start-here.md",
    "docs/onboarding/source-of-truth-map.md",
    "docs/onboarding/codex-navigation-map.md",
    "docs/onboarding/deep-research-handoff-map.md",
    "docs/onboarding/contributor-module-map.md",
    "docs/onboarding/private-generated-data-map.md",
    "docs/onboarding/operational-file-map.md",
    "docs/onboarding/source-harvester-workflow.md",
    "docs/onboarding/local-source-inventory-workflow.md",
    "tutorials/14-codex-assisted-development.md",
    "tutorials/15-troubleshooting.md",
    "docs/wiki-source/*",
    "data/project-state/*source-of-truth*.yaml",
    "data/source-harvester/stage5ag-source-harvester-summary.yaml",
    "data/source-harvester/stage5ag-source-harvester-next-stage-decision.yaml",
)

STRICT_PATHS = (
    "README.md",
    "STATUS.md",
    "ROADMAP.md",
    "AGENTS.md",
    "CUDA_NOTES.md",
    "BENCHMARKS.md",
    "EXPERIMENTS.md",
    "RESULTS_SCHEMA.md",
    "TESTING.md",
    "CIPHER_CATALOG.md",
    "docs/roadmap/staged-plan.md",
    "docs/onboarding/start-here.md",
    "docs/onboarding/source-of-truth-map.md",
    "docs/onboarding/codex-navigation-map.md",
    "docs/onboarding/deep-research-handoff-map.md",
    "docs/onboarding/contributor-module-map.md",
    "docs/onboarding/private-generated-data-map.md",
    "docs/onboarding/operational-file-map.md",
    "docs/onboarding/source-harvester-workflow.md",
    "docs/onboarding/local-source-inventory-workflow.md",
)


def build_operational_file_map_coverage(
    *,
    operational_file_map: Path,
) -> dict[str, Any]:
    """Return coverage findings for required operational files."""

    payload = yaml.safe_load(operational_file_map.read_text(encoding="utf-8")) or {}
    records = [record for record in payload.get("records", []) if isinstance(record, dict)]
    by_path = {str(record.get("path")): record for record in records}
    findings: list[dict[str, Any]] = []
    for required in REQUIRED_PATHS:
        if "*" in required:
            prefix = required.split("*", 1)[0]
            if not any(path.startswith(prefix) for path in by_path):
                findings.append(
                    {
                        "finding_id": f"missing_required_wildcard:{required}",
                        "rule_id": "missing_required_operational_wildcard",
                        "severity": "error",
                        "path": required,
                        "message": f"No operational-file-map record covers {required}.",
                    }
                )
            continue
        if required not in by_path:
            findings.append(
                {
                    "finding_id": f"missing_required_path:{required}",
                    "rule_id": "missing_required_operational_path",
                    "severity": "error",
                    "path": required,
                    "message": f"{required} is missing from operational-file-map records.",
                }
            )
    for strict_path in STRICT_PATHS:
        record = by_path.get(strict_path)
        if record and record.get("staleness_check_level") != "strict":
            findings.append(
                {
                    "finding_id": f"strict_required:{strict_path}",
                    "rule_id": "strict_coverage_required",
                    "severity": "error",
                    "path": strict_path,
                    "message": f"{strict_path} carries mutable current-state context and must be strict.",
                }
            )
    return {
        "record_type": "operational_file_map_coverage_report",
        "operational_file_map": str(operational_file_map).replace("\\", "/"),
        "record_count": len(records),
        "required_path_count": len(REQUIRED_PATHS),
        "strict_path_count": len(STRICT_PATHS),
        "coverage_finding_count": len(findings),
        "findings": findings,
    }
