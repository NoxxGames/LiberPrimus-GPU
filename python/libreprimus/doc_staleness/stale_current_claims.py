"""Tracked-file stale current/latest/next-stage claim scanner."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import re
import subprocess
from typing import Any

import yaml

from libreprimus.doc_staleness.stage_ids import StageId, find_stage_ids, parse_stage_id
from libreprimus.paths import repo_root

CURRENT_STAGE_STATE = Path("data/project-state/current-stage-state.yaml")
TEXT_EXTENSIONS = {
    ".md",
    ".txt",
    ".yaml",
    ".yml",
    ".json",
    ".toml",
    ".ps1",
    ".sh",
    ".py",
    ".rst",
    ".html",
}
EXCLUDED_PREFIXES = (
    ".git/",
    ".wiki-worktree/",
    "codex-output/",
    "experiments/results/",
    "third_party/",
    "data/raw/",
    "__pycache__/",
    ".venv/",
)
EXCLUDED_SUFFIXES = (
    ".sqlite",
    ".sqlite3",
    ".db",
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".pdf",
    ".zip",
    ".tar",
    ".7z",
    ".mp3",
    ".wav",
    ".bin",
)
CURRENT_MIRRORS = {
    "README.md",
    "STATUS.md",
    "ROADMAP.md",
    "docs/roadmap/staged-plan.md",
}
OPERATING_CONTEXT = {
    "AGENTS.md",
    "ChatGPT-ContextFile.md",
}
ONBOARDING_PREFIX = "docs/onboarding/"
HISTORICAL_PREFIXES = (
    "docs/development-logs/",
    "research-log/",
)
HISTORICAL_CONTEXT_RE = re.compile(
    r"\b(historical|history|at the time of|as of stage|after stage\s+\d|"
    r"completed stage timeline|development log|research log|evidence only|"
    r"local stage\s+\d+[a-z]*\s+summary)\b",
    re.IGNORECASE,
)
SUPPRESSION_RE = re.compile(
    r"doc-staleness:\s*allow-historical-current-phrase(?:;\s*reason:\s*(?P<reason>[^<\n]+))?",
    re.IGNORECASE,
)
MARKER_BEGIN_RE = re.compile(r"<!--\s*BEGIN\s+(?P<marker>stage\d+[a-z]+)\s*-->", re.IGNORECASE)
MARKER_END_RE = re.compile(r"<!--\s*END\s+(?P<marker>stage\d+[a-z]+)\s*-->", re.IGNORECASE)
HEADING_RE = re.compile(r"^(?P<marks>#{1,6})\s+(?P<title>.+?)\s*$")
HISTORICAL_SECTION_HEADING_RE = re.compile(
    r"\b(completed in stage|historical stage|stage\s+\d+[a-z]*\s+(?!current\b|current boundary\b))",
    re.IGNORECASE,
)
CURRENT_PHRASE_RE = re.compile(
    r"\b(latest completed stage|latest stage|current completed stage|current stage|"
    r"current state|current planning focus|next recommended prompt|next stage|next prompt)\b",
    re.IGNORECASE,
)
STAGE_IS_LATEST_RE = re.compile(
    r"\bStage\s+\d+[A-Z]*\s+is\s+the\s+latest\s+completed\s+stage\b",
    re.IGNORECASE,
)
STAGE_COMPLETE_NEXT_RE = re.compile(
    r"\bStage\s+\d+[A-Z]*\s+is\s+complete\s+and\s+Stage\s+\d+[A-Z]*\b.*\bnext\b",
    re.IGNORECASE,
)
STAGE_COMPLETE_RE = re.compile(
    r"\bStage\s+\d+[A-Z]*\b.{0,120}\bis\s+complete\b",
    re.IGNORECASE,
)
AFTER_STAGE_RE = re.compile(
    r"\bafter\s+Stage\s+\d+[A-Z]*\b",
    re.IGNORECASE,
)
STAGE_CURRENT_BOUNDARY_RE = re.compile(
    r"\bStage\s+\d+[A-Z]*\b.{0,80}\bcurrent\s+boundary\b",
    re.IGNORECASE,
)
CURRENT_BOUNDARY_HEADING_RE = re.compile(
    r"^\s*#{1,6}\s+Stage\s+\d+[A-Z]*\s+Current\s+Boundary\b",
    re.IGNORECASE,
)
COLON_CURRENT_RE = re.compile(
    r"\b(latest completed stage|latest stage|current completed stage|current stage|current state)\s*:\s*`?Stage\s+\d+[A-Z]*",
    re.IGNORECASE,
)
COLON_NEXT_RE = re.compile(
    r"\b(current next prompt|next recommended prompt|recommended next prompt|next prompt|"
    r"next stage|recommended next stage|selected next stage|selected next prompt|current routing)\s*:\s*`?Stage\s+\d+[A-Z]*",
    re.IGNORECASE,
)
CURRENT_PLANNING_RE = re.compile(
    r"\bcurrent planning focus\s*:\s*`?Stage\s+\d+[A-Z]*",
    re.IGNORECASE,
)
STAGE_SELECTS_NEXT_RE = re.compile(
    r"\bStage\s+\d+[A-Z]*\b.{0,80}\b(selects|selected|routes? to|routed to)\b"
    r".{0,80}\bStage\s+\d+[A-Z]*\b.{0,40}\bas\s+the\s+next\s+(prompt|stage)\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class StaleCurrentFinding:
    finding_id: str
    path: str
    line: int
    severity: str
    document_role: str
    claim_type: str
    matched_text: str
    expected_latest_stage: str
    expected_next_stage: str
    suggested_fix: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "path": self.path,
            "line": self.line,
            "severity": self.severity,
            "document_role": self.document_role,
            "claim_type": self.claim_type,
            "matched_text": self.matched_text,
            "expected_latest_stage": self.expected_latest_stage,
            "expected_next_stage": self.expected_next_stage,
            "suggested_fix": self.suggested_fix,
        }


@dataclass(frozen=True)
class StaleCurrentReport:
    expected_latest_stage: str
    expected_next_stage: str
    scanned_path_count: int
    skipped_path_count: int
    findings: tuple[StaleCurrentFinding, ...]
    warnings: tuple[str, ...] = ()

    @property
    def finding_count(self) -> int:
        return len(self.findings)

    @property
    def error_count(self) -> int:
        return sum(1 for finding in self.findings if finding.severity == "error")

    @property
    def warning_count(self) -> int:
        return sum(1 for finding in self.findings if finding.severity.startswith("warning"))

    @property
    def suppression_error_count(self) -> int:
        return sum(1 for finding in self.findings if finding.claim_type == "invalid_suppression")

    def to_dict(self) -> dict[str, Any]:
        return {
            "record_type": "stale_current_claim_report",
            "expected_latest_stage": self.expected_latest_stage,
            "expected_next_stage": self.expected_next_stage,
            "scanned_path_count": self.scanned_path_count,
            "skipped_path_count": self.skipped_path_count,
            "finding_count": self.finding_count,
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "suppression_error_count": self.suppression_error_count,
            "findings": [finding.to_dict() for finding in self.findings],
            "warnings": list(self.warnings),
        }


def load_current_truth(path: Path | str = CURRENT_STAGE_STATE) -> tuple[StageId, StageId]:
    payload = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    latest_text = str(
        payload.get("latest_completed_stage_title")
        or payload.get("latest_completed_stage_id")
        or payload.get("stage_id")
    )
    next_text = str(payload.get("recommended_next_stage_title") or payload.get("recommended_next_stage_id"))
    return parse_stage_id(latest_text), parse_stage_id(next_text)


def audit_repository(
    *,
    root: Path | None = None,
    current_stage_state: Path | str = CURRENT_STAGE_STATE,
    expected_latest_stage: str | None = None,
    expected_next_stage: str | None = None,
    include_untracked_paths: list[Path] | None = None,
) -> StaleCurrentReport:
    base = root or repo_root()
    latest, next_stage = load_current_truth(base / current_stage_state)
    if expected_latest_stage:
        latest = parse_stage_id(expected_latest_stage)
    if expected_next_stage:
        next_stage = parse_stage_id(expected_next_stage)

    paths = _tracked_text_paths(base)
    for path in include_untracked_paths or []:
        relative = _relative_path(path, base)
        if _is_text_like(relative) and not _is_excluded(relative) and relative not in paths:
            paths.append(relative)
    paths = sorted(paths)

    findings: list[StaleCurrentFinding] = []
    warnings: list[str] = []
    scanned = 0
    skipped = 0
    for relative in paths:
        if _is_excluded(relative):
            skipped += 1
            continue
        path = base / relative
        if not path.is_file():
            skipped += 1
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            skipped += 1
            warnings.append(f"non_utf8_skipped:{relative}")
            continue
        scanned += 1
        findings.extend(scan_text(text, relative, latest, next_stage))

    return StaleCurrentReport(
        expected_latest_stage=latest.label,
        expected_next_stage=next_stage.label,
        scanned_path_count=scanned,
        skipped_path_count=skipped,
        findings=tuple(sorted(findings, key=lambda item: (item.path, item.line, item.claim_type))),
        warnings=tuple(sorted(warnings)),
    )


def scan_text(
    text: str,
    path: str,
    expected_latest_stage: StageId,
    expected_next_stage: StageId,
) -> list[StaleCurrentFinding]:
    lines = text.splitlines()
    findings: list[StaleCurrentFinding] = []
    historical_marker_depth = 0
    historical_heading_level: int | None = None
    for index, line in enumerate(lines, start=1):
        heading_match = HEADING_RE.match(line)
        if heading_match:
            heading_level = len(heading_match.group("marks"))
            heading_title = heading_match.group("title")
            if historical_heading_level is not None and heading_level <= historical_heading_level:
                historical_heading_level = None
            if HISTORICAL_SECTION_HEADING_RE.search(heading_title):
                historical_heading_level = heading_level
        begin_marker = MARKER_BEGIN_RE.search(line)
        if begin_marker:
            try:
                marker_stage = parse_stage_id(begin_marker.group("marker"))
                if marker_stage != expected_latest_stage:
                    historical_marker_depth += 1
            except ValueError:
                pass
        if historical_marker_depth > 0:
            if MARKER_END_RE.search(line):
                historical_marker_depth = max(0, historical_marker_depth - 1)
            continue
        if historical_heading_level is not None:
            continue
        suppression = SUPPRESSION_RE.search(line) if _is_suppression_directive(line) else None
        if suppression and not (suppression.group("reason") or "").strip():
            findings.append(
                _finding(
                    path,
                    index,
                    "error",
                    "invalid_suppression",
                    line,
                    expected_latest_stage,
                    expected_next_stage,
                )
            )
            continue
        if _has_reasoned_suppression(lines, index):
            continue
        if _is_explicitly_historical(line):
            continue
        claim_type = _claim_type(line)
        if not claim_type:
            continue
        stages = find_stage_ids(line)
        if _line_matches_expected(line, claim_type, stages, expected_latest_stage, expected_next_stage):
            continue
        if not stages and claim_type != "current_boundary_heading":
            continue
        findings.append(
            _finding(
                path,
                index,
                _severity(path, claim_type),
                claim_type,
                line,
                expected_latest_stage,
                expected_next_stage,
            )
        )
        if MARKER_END_RE.search(line):
            historical_marker_depth = max(0, historical_marker_depth - 1)
    return findings


def write_report(path: Path, report: StaleCurrentReport) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _tracked_text_paths(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    return [line.strip().replace("\\", "/") for line in result.stdout.splitlines() if _is_text_like(line.strip())]


def _is_text_like(relative: str) -> bool:
    normalized = relative.replace("\\", "/")
    suffix = Path(normalized).suffix.lower()
    return suffix in TEXT_EXTENSIONS and not normalized.endswith(EXCLUDED_SUFFIXES)


def _is_excluded(relative: str) -> bool:
    normalized = relative.replace("\\", "/")
    return normalized.endswith(EXCLUDED_SUFFIXES) or any(
        normalized == prefix.rstrip("/") or normalized.startswith(prefix) for prefix in EXCLUDED_PREFIXES
    )


def _relative_path(path: Path, root: Path) -> str:
    resolved = path if not path.is_absolute() else path.resolve()
    try:
        return resolved.relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _claim_type(line: str) -> str | None:
    if CURRENT_BOUNDARY_HEADING_RE.search(line):
        return "current_boundary_heading"
    lower = line.lower()
    if CURRENT_PLANNING_RE.search(line):
        return "current_planning_focus_claim"
    if STAGE_COMPLETE_NEXT_RE.search(line):
        return "complete_and_next_claim"
    if STAGE_CURRENT_BOUNDARY_RE.search(line):
        return "current_boundary_reference_claim"
    if AFTER_STAGE_RE.search(line):
        return "after_stage_current_boundary_claim"
    if STAGE_COMPLETE_RE.search(line):
        return "stage_complete_claim"
    if STAGE_IS_LATEST_RE.search(line) or COLON_CURRENT_RE.search(line):
        return "latest_completed_stage_claim"
    if COLON_NEXT_RE.search(line) or STAGE_SELECTS_NEXT_RE.search(line):
        return "next_stage_claim"
    if "current state" in lower and STAGE_COMPLETE_NEXT_RE.search(line):
        return "current_state_claim"
    if CURRENT_PHRASE_RE.search(line) and COLON_CURRENT_RE.search(line):
        return "current_like_claim"
    return None


def _line_matches_expected(
    line: str,
    claim_type: str,
    stages: list[StageId],
    expected_latest_stage: StageId,
    expected_next_stage: StageId,
) -> bool:
    lower = line.lower()
    if claim_type == "current_boundary_heading":
        return expected_latest_stage in stages
    if "planning focus" in lower or claim_type == "next_stage_claim":
        return any(stage == expected_next_stage for stage in stages)
    if claim_type in {"complete_and_next_claim"}:
        return expected_latest_stage in stages and expected_next_stage in stages
    if claim_type in {
        "latest_completed_stage_claim",
        "current_state_claim",
        "current_like_claim",
        "current_boundary_reference_claim",
        "after_stage_current_boundary_claim",
        "stage_complete_claim",
    }:
        return expected_latest_stage in stages or expected_next_stage in stages
    return False


def _is_explicitly_historical(line: str) -> bool:
    return bool(HISTORICAL_CONTEXT_RE.search(line))


def _has_reasoned_suppression(lines: list[str], one_based_line: int) -> bool:
    for offset in (-1, 0, 1):
        position = one_based_line - 1 + offset
        if 0 <= position < len(lines):
            match = SUPPRESSION_RE.search(lines[position]) if _is_suppression_directive(lines[position]) else None
            if match and (match.group("reason") or "").strip():
                return True
    return False


def _is_suppression_directive(line: str) -> bool:
    stripped = line.lstrip()
    return stripped.startswith(("<!--", "#", "//")) and bool(SUPPRESSION_RE.search(line))


def _document_role(path: str) -> str:
    normalized = path.replace("\\", "/")
    if normalized in CURRENT_MIRRORS:
        return "current_mirror"
    if normalized in OPERATING_CONTEXT:
        return "operating_context"
    if normalized.startswith(ONBOARDING_PREFIX):
        return "onboarding_doc"
    if normalized.startswith(HISTORICAL_PREFIXES):
        return "historical_log_or_stage_evidence"
    if normalized.startswith("data/project-state/"):
        return "machine_registry"
    return "domain_doc"


def _severity(path: str, claim_type: str) -> str:
    role = _document_role(path)
    if role in {"current_mirror", "operating_context", "onboarding_doc"}:
        return "error"
    if role == "historical_log_or_stage_evidence":
        return "warning_historical_unlabeled"
    if claim_type in {"current_planning_focus_claim", "current_state_claim", "latest_completed_stage_claim"}:
        return "warning_domain_current_claim"
    return "warning_domain"


def _finding(
    path: str,
    line_no: int,
    severity: str,
    claim_type: str,
    line: str,
    expected_latest_stage: StageId,
    expected_next_stage: StageId,
) -> StaleCurrentFinding:
    return StaleCurrentFinding(
        finding_id=f"{claim_type}:{path}:{line_no}",
        path=path,
        line=line_no,
        severity=severity,
        document_role=_document_role(path),
        claim_type=claim_type,
        matched_text=line.strip(),
        expected_latest_stage=expected_latest_stage.label,
        expected_next_stage=expected_next_stage.label,
        suggested_fix=_suggested_fix(claim_type, expected_latest_stage, expected_next_stage),
    )


def _suggested_fix(claim_type: str, latest: StageId, next_stage: StageId) -> str:
    if claim_type == "current_boundary_heading":
        return "Rename the heading to Historical Stage X Boundary or update it to the true current stage."
    if claim_type == "next_stage_claim":
        return f"Use {next_stage.label} for current next-stage claims or mark the sentence historical."
    if claim_type == "complete_and_next_claim":
        return f"Use {latest.label} complete and {next_stage.label} next, or mark the sentence historical."
    return f"Use {latest.label} for current/latest claims or mark the sentence historical."
