"""Models for operational Markdown staleness scanning."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


DEFAULT_SOURCE_OF_TRUTH = Path("data/project-state/stage5ab-doc-staleness-source-of-truth.yaml")
DEFAULT_OPERATIONAL_FILE_MAP = Path("data/project-state/operational-file-map.yaml")

DEFAULT_OPERATIONAL_PATHS = (
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
    "tutorials/10-hardware-and-performance.md",
    "tutorials/14-codex-assisted-development.md",
    "tutorials/15-troubleshooting.md",
)

HISTORICAL_PATH_PREFIXES = (
    "docs/development-logs/",
    "research-log/",
    "codex-output/",
)


@dataclass(frozen=True)
class SourceOfTruth:
    stage_id: str
    latest_completed_stage_after_this_stage: str
    next_stage_after_this_stage: str
    latest_previous_stage: str
    user_override_reason: str
    website_expansion_status: str
    scored_experiments_status: str
    unsolved_page_cuda_status: str
    canonical_corpus_status: str
    page_boundaries_status: str
    expected_next_stage_prefix: str
    latest_completed_stage_prefix: str

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "SourceOfTruth":
        return cls(
            stage_id=str(payload["stage_id"]),
            latest_completed_stage_after_this_stage=str(
                payload["latest_completed_stage_after_this_stage"]
            ),
            next_stage_after_this_stage=str(payload["next_stage_after_this_stage"]),
            latest_previous_stage=str(payload["latest_previous_stage"]),
            user_override_reason=str(payload["user_override_reason"]),
            website_expansion_status=str(payload["website_expansion_status"]),
            scored_experiments_status=str(payload["scored_experiments_status"]),
            unsolved_page_cuda_status=str(payload["unsolved_page_cuda_status"]),
            canonical_corpus_status=str(payload["canonical_corpus_status"]),
            page_boundaries_status=str(payload["page_boundaries_status"]),
            expected_next_stage_prefix=str(payload["expected_next_stage_prefix"]),
            latest_completed_stage_prefix=str(payload["latest_completed_stage_prefix"]),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage_id": self.stage_id,
            "latest_completed_stage_after_this_stage": (
                self.latest_completed_stage_after_this_stage
            ),
            "next_stage_after_this_stage": self.next_stage_after_this_stage,
            "latest_previous_stage": self.latest_previous_stage,
            "user_override_reason": self.user_override_reason,
            "website_expansion_status": self.website_expansion_status,
            "scored_experiments_status": self.scored_experiments_status,
            "unsolved_page_cuda_status": self.unsolved_page_cuda_status,
            "canonical_corpus_status": self.canonical_corpus_status,
            "page_boundaries_status": self.page_boundaries_status,
            "expected_next_stage_prefix": self.expected_next_stage_prefix,
            "latest_completed_stage_prefix": self.latest_completed_stage_prefix,
        }


@dataclass(frozen=True)
class StalenessFinding:
    finding_id: str
    rule_id: str
    severity: str
    path: str
    line: int
    message: str
    excerpt: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "rule_id": self.rule_id,
            "severity": self.severity,
            "path": self.path,
            "line": self.line,
            "message": self.message,
            "excerpt": self.excerpt,
        }


@dataclass(frozen=True)
class ScanResult:
    source_of_truth: SourceOfTruth
    scanned_paths: tuple[str, ...]
    findings: tuple[StalenessFinding, ...]
    warnings: tuple[str, ...] = field(default_factory=tuple)

    @property
    def finding_count(self) -> int:
        return len(self.findings)

    @property
    def files_with_findings(self) -> tuple[str, ...]:
        return tuple(sorted({finding.path for finding in self.findings}))

    def summary_dict(self) -> dict[str, Any]:
        return {
            "record_type": "doc_staleness_scan_summary",
            "source_of_truth_stage_id": self.source_of_truth.stage_id,
            "latest_completed_stage": (
                self.source_of_truth.latest_completed_stage_after_this_stage
            ),
            "next_stage": self.source_of_truth.next_stage_after_this_stage,
            "scanned_path_count": len(self.scanned_paths),
            "finding_count": self.finding_count,
            "files_with_findings": list(self.files_with_findings),
            "warning_count": len(self.warnings),
            "warnings": list(self.warnings),
        }
