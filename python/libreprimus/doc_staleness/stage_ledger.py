"""Stage-ledger staleness checks for mutable operational docs."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any

from libreprimus.doc_staleness.stage_ids import StageId, find_stage_ids, parse_stage_id

LEDGER_HEADING_RE = re.compile(
    r"(already implemented|completed stages|current status|stage history|latest stages|"
    r"current boundaries|deferred work|current work)",
    re.IGNORECASE,
)
EXEMPT_HEADING_RE = re.compile(
    r"(historical snapshot|selected highlights|not exhaustive|excerpt|archive|troubleshooting|"
    r"\brules\b|^phase\s+\d|boundary|cuda planning)",
    re.IGNORECASE,
)
STAGE_LINE_RE = re.compile(r"^\s*(?:[-*]\s+)?(?:Stage|stage)[\s-]*\d+[A-Za-z]*\b")
HEADING_RE = re.compile(r"^(?P<marks>#{1,6})\s+(?P<title>.+?)\s*$")


@dataclass(frozen=True)
class StageLedgerFinding:
    """A stale stage-ledger finding."""

    finding_id: str
    rule_id: str
    severity: str
    path: str
    line: int
    section_title: str
    message: str
    max_stage: str
    expected_stage: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "rule_id": self.rule_id,
            "severity": self.severity,
            "path": self.path,
            "line": self.line,
            "section_title": self.section_title,
            "message": self.message,
            "max_stage": self.max_stage,
            "expected_stage": self.expected_stage,
        }


@dataclass(frozen=True)
class StageLedgerSection:
    """A possible stage-ledger section."""

    path: str
    title: str
    line: int
    stage_count: int
    max_stage: StageId | None
    exempt: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "title": self.title,
            "line": self.line,
            "stage_count": self.stage_count,
            "max_stage": self.max_stage.label if self.max_stage else None,
            "exempt": self.exempt,
        }


def scan_stage_ledgers(
    *,
    paths: tuple[str, ...],
    root: Path,
    expected_latest_stage: str,
) -> dict[str, Any]:
    """Scan mutable operational docs for stale stage-ledger sections."""

    expected = parse_stage_id(expected_latest_stage)
    sections: list[StageLedgerSection] = []
    findings: list[StageLedgerFinding] = []
    warnings: list[str] = []
    for relative in paths:
        path = root / relative
        if not path.is_file():
            warnings.append(f"missing_operational_file:{relative}")
            continue
        file_sections = _sections_for_text(path.read_text(encoding="utf-8"), relative)
        sections.extend(file_sections)
        for section in file_sections:
            if section.exempt or section.max_stage is None or section.stage_count < 5:
                continue
            if section.max_stage < expected:
                findings.append(
                    StageLedgerFinding(
                        finding_id=f"stale_stage_ledger:{section.path}:{section.line}",
                        rule_id="stale_stage_ledger_truncation",
                        severity="error",
                        path=section.path,
                        line=section.line,
                        section_title=section.title,
                        message=(
                            f"Stage ledger section ends at {section.max_stage.label}; "
                            f"expected at least {expected.label}."
                        ),
                        max_stage=section.max_stage.label,
                        expected_stage=expected.label,
                    )
                )
    return {
        "record_type": "stage_ledger_staleness_report",
        "expected_latest_stage": expected.label,
        "sections_scanned": len(sections),
        "sections": [section.to_dict() for section in sections],
        "finding_count": len(findings),
        "findings": [finding.to_dict() for finding in findings],
        "warning_count": len(warnings),
        "warnings": warnings,
    }


def stage_ledger_findings_for_text(
    text: str,
    *,
    path: str = "README.md",
    expected_latest_stage: str,
) -> list[StageLedgerFinding]:
    """Return stale stage-ledger findings for one text payload."""

    expected = parse_stage_id(expected_latest_stage)
    findings: list[StageLedgerFinding] = []
    for section in _sections_for_text(text, path):
        if section.exempt or section.max_stage is None or section.stage_count < 5:
            continue
        if section.max_stage < expected:
            findings.append(
                StageLedgerFinding(
                    finding_id=f"stale_stage_ledger:{section.path}:{section.line}",
                    rule_id="stale_stage_ledger_truncation",
                    severity="error",
                    path=section.path,
                    line=section.line,
                    section_title=section.title,
                    message=(
                        f"Stage ledger section ends at {section.max_stage.label}; "
                        f"expected at least {expected.label}."
                    ),
                    max_stage=section.max_stage.label,
                    expected_stage=expected.label,
                )
            )
    return findings


def _sections_for_text(text: str, path: str) -> list[StageLedgerSection]:
    lines = text.splitlines()
    heading_indexes: list[tuple[int, int, str]] = []
    for index, line in enumerate(lines):
        match = HEADING_RE.match(line)
        if match:
            heading_indexes.append((index, len(match.group("marks")), match.group("title").strip()))
    sections: list[StageLedgerSection] = []
    for position, (index, level, title) in enumerate(heading_indexes):
        if not LEDGER_HEADING_RE.search(title) and not _body_looks_like_stage_ledger(lines[index + 1 :]):
            continue
        end = len(lines)
        for next_index, next_level, _next_title in heading_indexes[position + 1 :]:
            if next_level <= level:
                end = next_index
                break
        body = lines[index + 1 : end]
        stages = _stage_ids_in_section(body)
        if len(stages) < 5 and not LEDGER_HEADING_RE.search(title):
            continue
        max_stage = max(stages) if stages else None
        section_text = "\n".join([title, *body[:3]])
        sections.append(
            StageLedgerSection(
                path=path,
                title=title,
                line=index + 1,
                stage_count=len(stages),
                max_stage=max_stage,
                exempt=bool(EXEMPT_HEADING_RE.search(section_text)),
            )
        )
    return sections


def _body_looks_like_stage_ledger(lines: list[str]) -> bool:
    stage_lines = 0
    for line in lines[:80]:
        if not line.strip():
            continue
        if HEADING_RE.match(line):
            break
        if STAGE_LINE_RE.match(line):
            stage_lines += 1
    return stage_lines >= 5


def _stage_ids_in_section(lines: list[str]) -> list[StageId]:
    stages: list[StageId] = []
    for line in lines:
        if STAGE_LINE_RE.match(line) or LEDGER_HEADING_RE.search(line):
            stages.extend(find_stage_ids(line))
    return stages
