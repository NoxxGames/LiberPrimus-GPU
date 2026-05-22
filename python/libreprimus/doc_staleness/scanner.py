"""Operational Markdown staleness scanner."""

from __future__ import annotations

from pathlib import Path
import re

from libreprimus.doc_staleness.models import (
    HISTORICAL_PATH_PREFIXES,
    ScanResult,
    SourceOfTruth,
    StalenessFinding,
)
from libreprimus.doc_staleness.source_of_truth import (
    load_operational_paths,
    load_source_of_truth,
)
from libreprimus.doc_staleness.stage_ids import StageId, find_stage_ids, parse_stage_id
from libreprimus.paths import repo_root

WEBSITE_STAGE6_RE = re.compile(
    r"Website expansion is deferred to Stage 6|website_stage6|Stage 6 - website expansion",
    re.IGNORECASE,
)
NEXT_LABEL_RE = re.compile(
    r"\bnext(?:\s+(?:recommended prompt|planned stage|stage|selected stage))?\s*:\s*",
    re.IGNORECASE,
)
CURRENT_LABEL_RE = re.compile(
    r"\b(?:current completed stage|latest completed stage|current work|current planning focus)"
    r"\s*:\s*",
    re.IGNORECASE,
)
CUDA_CAP_RE = re.compile(r"\bExisting CUDA code\b.*\bonly\b", re.IGNORECASE)
HISTORICAL_LINE_RE = re.compile(
    r"\b(historical|completed in stage|completed stage timeline|already implemented|archive|"
    r"development log|research log|stage details|source-of-truth summary)\b",
    re.IGNORECASE,
)


def scan_repository(
    *,
    root: Path | None = None,
    source_of_truth_path: Path | str | None = None,
    operational_file_map: Path | str | None = None,
) -> ScanResult:
    base = root or repo_root()
    source = load_source_of_truth(source_of_truth_path, root=base)
    paths = load_operational_paths(operational_file_map, root=base)
    findings: list[StalenessFinding] = []
    warnings: list[str] = []
    scanned: list[str] = []

    for relative in paths:
        path = base / relative
        if _is_historical_path(relative):
            continue
        if not path.is_file():
            warnings.append(f"missing_operational_file:{relative}")
            continue
        scanned.append(relative)
        findings.extend(_scan_text(path.read_text(encoding="utf-8"), relative, source))

    return ScanResult(
        source_of_truth=source,
        scanned_paths=tuple(scanned),
        findings=tuple(findings),
        warnings=tuple(warnings),
    )


def scan_text(text: str, path: str, source: SourceOfTruth) -> list[StalenessFinding]:
    """Scan a single text payload. Intended for tests and focused callers."""

    return _scan_text(text, path, source)


def _scan_text(text: str, relative: str, source: SourceOfTruth) -> list[StalenessFinding]:
    if _is_historical_path(relative):
        return []
    findings: list[StalenessFinding] = []
    expected_next = parse_stage_id(source.expected_next_stage_prefix)
    latest = parse_stage_id(source.latest_completed_stage_prefix)
    for line_no, line in enumerate(text.splitlines(), start=1):
        if _is_historical_line(line):
            continue
        findings.extend(_website_findings(relative, line_no, line))
        findings.extend(_current_next_findings(relative, line_no, line, expected_next, latest))
        findings.extend(_cuda_cap_findings(relative, line_no, line, latest))
    return findings


def _website_findings(relative: str, line_no: int, line: str) -> list[StalenessFinding]:
    if not WEBSITE_STAGE6_RE.search(line):
        return []
    return [
        _finding(
            "website_stage6_deferral",
            relative,
            line_no,
            "Website expansion must be deferred to a future unnumbered project, not Stage 6.",
            line,
        )
    ]


def _current_next_findings(
    relative: str,
    line_no: int,
    line: str,
    expected_next: StageId,
    latest: StageId,
) -> list[StalenessFinding]:
    stripped = line.strip()
    findings: list[StalenessFinding] = []
    if NEXT_LABEL_RE.search(stripped):
        if expected_next.label.lower() in stripped.lower():
            return findings
        for stage in find_stage_ids(stripped):
            if stage < expected_next:
                findings.append(
                    _finding(
                        "stale_next_stage_claim",
                        relative,
                        line_no,
                        f"Next-stage claim points to {stage.label}, older than {expected_next.label}.",
                        line,
                    )
                )
    if CURRENT_LABEL_RE.search(stripped):
        target = expected_next if "current work" in stripped.lower() or "planning focus" in stripped.lower() else latest
        if target.label.lower() in stripped.lower():
            return findings
        for stage in find_stage_ids(stripped):
            if stage != target:
                findings.append(
                    _finding(
                        "stale_current_stage_claim",
                        relative,
                        line_no,
                        f"Current-state claim points to {stage.label}; expected {target.label}.",
                        line,
                    )
                )
    return findings


def _cuda_cap_findings(
    relative: str,
    line_no: int,
    line: str,
    latest: StageId,
) -> list[StalenessFinding]:
    if not CUDA_CAP_RE.search(line):
        return []
    lower = line.lower()
    if "latest staged-plan and cuda notes" in lower:
        return []
    if latest.label.lower() in lower:
        return []
    return [
        _finding(
            "stale_existing_cuda_code_cap",
            relative,
            line_no,
            "Current Existing CUDA code cap omits the latest completed stage or uses brittle only wording.",
            line,
        )
    ]


def _finding(
    rule_id: str,
    relative: str,
    line_no: int,
    message: str,
    line: str,
) -> StalenessFinding:
    return StalenessFinding(
        finding_id=f"{rule_id}:{relative}:{line_no}",
        rule_id=rule_id,
        severity="error",
        path=relative,
        line=line_no,
        message=message,
        excerpt=line.strip(),
    )


def _is_historical_path(relative: str) -> bool:
    normalized = relative.replace("\\", "/")
    return any(normalized.startswith(prefix) for prefix in HISTORICAL_PATH_PREFIXES)


def _is_historical_line(line: str) -> bool:
    return bool(HISTORICAL_LINE_RE.search(line))
