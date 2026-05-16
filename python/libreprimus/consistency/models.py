"""Models for Stage 2D consistency check results."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Any


class ConsistencyCheckStatus(StrEnum):
    PASS = "pass"
    FAIL = "fail"
    WARNING = "warning"
    SKIPPED = "skipped"


class ConsistencyCheckSeverity(StrEnum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclass(frozen=True)
class ConsistencyWarning:
    message: str
    check_group: str
    path: str | None = None


@dataclass(frozen=True)
class ConsistencyError:
    message: str
    check_group: str
    path: str | None = None


@dataclass(frozen=True)
class ConsistencyCheckResult:
    check_group: str
    check_name: str
    status: ConsistencyCheckStatus
    severity: ConsistencyCheckSeverity
    message: str
    path: str | None = None
    data: dict[str, Any] = field(default_factory=dict)

    @property
    def is_failure(self) -> bool:
        return self.status == ConsistencyCheckStatus.FAIL or self.severity == ConsistencyCheckSeverity.ERROR

    @property
    def is_warning(self) -> bool:
        return self.status == ConsistencyCheckStatus.WARNING

    def to_dict(self) -> dict[str, Any]:
        return {
            "check_group": self.check_group,
            "check_name": self.check_name,
            "status": self.status.value,
            "severity": self.severity.value,
            "message": self.message,
            "path": self.path,
            "data": self.data,
        }


@dataclass(frozen=True)
class ConsistencyCheckSuiteResult:
    suite_id: str
    results: list[ConsistencyCheckResult]

    @property
    def pass_count(self) -> int:
        return self._count(ConsistencyCheckStatus.PASS)

    @property
    def fail_count(self) -> int:
        return self._count(ConsistencyCheckStatus.FAIL)

    @property
    def warning_count(self) -> int:
        return self._count(ConsistencyCheckStatus.WARNING)

    @property
    def skipped_count(self) -> int:
        return self._count(ConsistencyCheckStatus.SKIPPED)

    @property
    def check_count(self) -> int:
        return len(self.results)

    @property
    def has_failures(self) -> bool:
        return any(result.is_failure for result in self.results)

    @property
    def has_warnings(self) -> bool:
        return any(result.is_warning for result in self.results)

    def _count(self, status: ConsistencyCheckStatus) -> int:
        return sum(1 for result in self.results if result.status == status)

    def to_dict(self) -> dict[str, Any]:
        return {
            "record_type": "consistency_check_suite_result",
            "suite_id": self.suite_id,
            "check_count": self.check_count,
            "pass_count": self.pass_count,
            "fail_count": self.fail_count,
            "warning_count": self.warning_count,
            "skipped_count": self.skipped_count,
            "results": [result.to_dict() for result in self.results],
        }


def pass_result(
    group: str,
    name: str,
    message: str,
    *,
    path: Path | str | None = None,
    data: dict[str, Any] | None = None,
) -> ConsistencyCheckResult:
    return ConsistencyCheckResult(
        check_group=group,
        check_name=name,
        status=ConsistencyCheckStatus.PASS,
        severity=ConsistencyCheckSeverity.INFO,
        message=message,
        path=str(path) if path is not None else None,
        data=data or {},
    )


def fail_result(
    group: str,
    name: str,
    message: str,
    *,
    path: Path | str | None = None,
    data: dict[str, Any] | None = None,
) -> ConsistencyCheckResult:
    return ConsistencyCheckResult(
        check_group=group,
        check_name=name,
        status=ConsistencyCheckStatus.FAIL,
        severity=ConsistencyCheckSeverity.ERROR,
        message=message,
        path=str(path) if path is not None else None,
        data=data or {},
    )


def warning_result(
    group: str,
    name: str,
    message: str,
    *,
    path: Path | str | None = None,
    data: dict[str, Any] | None = None,
) -> ConsistencyCheckResult:
    return ConsistencyCheckResult(
        check_group=group,
        check_name=name,
        status=ConsistencyCheckStatus.WARNING,
        severity=ConsistencyCheckSeverity.WARNING,
        message=message,
        path=str(path) if path is not None else None,
        data=data or {},
    )


def skipped_result(
    group: str,
    name: str,
    message: str,
    *,
    path: Path | str | None = None,
    data: dict[str, Any] | None = None,
) -> ConsistencyCheckResult:
    return ConsistencyCheckResult(
        check_group=group,
        check_name=name,
        status=ConsistencyCheckStatus.SKIPPED,
        severity=ConsistencyCheckSeverity.INFO,
        message=message,
        path=str(path) if path is not None else None,
        data=data or {},
    )
