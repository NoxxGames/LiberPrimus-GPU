"""Models for Stage 3E method backlog dry-runs."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class MethodBacklog:
    payload: dict[str, Any]
    path: str
    sha256: str

    @property
    def items(self) -> list[dict[str, Any]]:
        return [dict(item) for item in self.payload.get("items", [])]


@dataclass(frozen=True)
class Stage3EDryRunResult:
    item_id: str
    experiment_kind: str
    declared_candidate_count: int
    calculated_candidate_count: int
    policy_status: str
    implementation_status: str
    executor_status: str
    executable_now: bool
    blocking_reasons: list[str]
    warnings: list[str]


@dataclass(frozen=True)
class Stage3EDryRunSummary:
    queue_id: str
    policy_id: str
    item_count: int
    total_candidate_estimate: int
    runnable_now_count: int
    needs_executor_count: int
    dry_run_only_count: int
    blocked_count: int
    executed_count: int
    results: list[Stage3EDryRunResult]
    output_path: Path | None = None
