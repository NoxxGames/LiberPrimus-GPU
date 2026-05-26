"""Models and constants for the Stage 5AX validation harness."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

ParallelClass = Literal[
    "read_only_parallel_safe",
    "read_only_parallel_safe_with_isolated_temp",
    "serial_read_only_final_check",
    "serial_generates_outputs",
    "serial_git_mutating",
    "serial_remote_or_network",
    "serial_manual_only",
    "blocked",
]

PARALLEL_SAFE_CLASSES = {
    "read_only_parallel_safe",
    "read_only_parallel_safe_with_isolated_temp",
}

SERIAL_ONLY_CLASSES = {
    "serial_read_only_final_check",
    "serial_generates_outputs",
    "serial_git_mutating",
    "serial_remote_or_network",
    "serial_manual_only",
    "blocked",
}

STAGE_ID = "stage-5ax"
STAGE_TITLE = "Stage 5AX - parallel validation harness and fast CI check orchestrator"
NEXT_STAGE_TITLE = "Stage 5AY - bounded token-block preflight manifest design without execution"

PLAN_PATH = Path("data/ci/stage5ax-parallel-validation-plan.yaml")
COMMAND_REGISTRY_PATH = Path("data/ci/stage5ax-parallel-command-registry.yaml")
RUN_POLICY_PATH = Path("data/ci/stage5ax-parallel-run-policy.yaml")
RUN_SUMMARY_PATH = Path("data/ci/stage5ax-parallel-validation-run-summary.yaml")
SAFETY_AUDIT_PATH = Path("data/ci/stage5ax-parallel-validation-safety-audit.yaml")
PYTEST_SHARD_PLAN_PATH = Path("data/ci/stage5ax-pytest-shard-plan.yaml")
GUARDRAIL_PATH = Path("data/ci/stage5ax-guardrail.yaml")
NEXT_STAGE_DECISION_PATH = Path("data/project-state/stage5ax-next-stage-decision.yaml")
SUMMARY_PATH = Path("data/project-state/stage5ax-summary.yaml")
DEFAULT_RESULTS_DIR = Path("experiments/results/ci/parallel-validation/stage5ax")


@dataclass(frozen=True)
class ValidationCommand:
    """One command in the Stage 5AX classified validation registry."""

    command_id: str
    display_name: str
    command: list[str]
    working_directory: str = "."
    category: str = "validation"
    parallel_class: ParallelClass = "blocked"
    writes_outputs: bool = False
    writes_repo: bool = False
    uses_network: bool = False
    uses_git_mutation: bool = False
    uses_github_mutation: bool = False
    requires_serial: bool = True
    timeout_seconds: int = 600
    env: dict[str, str] = field(default_factory=dict)
    depends_on: list[str] = field(default_factory=list)
    allowed_in_ci: bool = True
    allowed_in_codex_local: bool = True
    notes: str = ""

    @property
    def parallel_safe(self) -> bool:
        return self.parallel_class in PARALLEL_SAFE_CLASSES and not self.requires_serial

    def to_record(self) -> dict[str, Any]:
        return {
            "command_id": self.command_id,
            "display_name": self.display_name,
            "command": self.command,
            "working_directory": self.working_directory,
            "category": self.category,
            "parallel_class": self.parallel_class,
            "writes_outputs": self.writes_outputs,
            "writes_repo": self.writes_repo,
            "uses_network": self.uses_network,
            "uses_git_mutation": self.uses_git_mutation,
            "uses_github_mutation": self.uses_github_mutation,
            "requires_serial": self.requires_serial,
            "timeout_seconds": self.timeout_seconds,
            "env": self.env,
            "depends_on": self.depends_on,
            "allowed_in_ci": self.allowed_in_ci,
            "allowed_in_codex_local": self.allowed_in_codex_local,
            "notes": self.notes,
        }


@dataclass(frozen=True)
class CommandResult:
    """Captured result for one subprocess command."""

    command_id: str
    display_name: str
    returncode: int
    duration_seconds: float
    stdout_log: str
    stderr_log: str
    timed_out: bool = False

    @property
    def passed(self) -> bool:
        return self.returncode == 0 and not self.timed_out

    def to_record(self) -> dict[str, Any]:
        return {
            "command_id": self.command_id,
            "display_name": self.display_name,
            "returncode": self.returncode,
            "duration_seconds": round(self.duration_seconds, 6),
            "stdout_log": self.stdout_log,
            "stderr_log": self.stderr_log,
            "timed_out": self.timed_out,
            "passed": self.passed,
        }
