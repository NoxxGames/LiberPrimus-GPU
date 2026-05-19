"""Path sanitisation and documentation freshness checks for committed records."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import subprocess

from libreprimus.paths import repo_root

LOCAL_PATH_PATTERNS = (
    re.compile(r"\b[A-Za-z]:\\[^\s)`>\"']+"),
    re.compile(r"\\\\[A-Za-z0-9_.-]+\\[^\s)`>\"']+"),
    re.compile(r"/home/[^/\s]+/[^\s)`>\"']+"),
    re.compile(r"/Users/[^/\s]+/[^\s)`>\"']+"),
)

STALE_OPERATIONAL_PATTERNS = (
    re.compile(r"Next:\s*Stage\s+4I\b", re.IGNORECASE),
    re.compile(r"Stage\s+3Z\s+current\b", re.IGNORECASE),
    re.compile(r"Stage\s+3Y\s+is\s+the\s+latest\s+completed\b", re.IGNORECASE),
    re.compile(r"Deferred\s+work\s+after\s+Stage\s+4D", re.IGNORECASE),
    re.compile(r"Stage\s+0A\s+scaffold", re.IGNORECASE),
)

SKIP_PATH_PARTS = (
    "docs/development-logs/",
    "research-log/",
    "docs/research/",
    "data/raw/",
    "data/normalized/",
    ".venv/",
    ".wiki-worktree/",
)

OPERATIONAL_SUFFIXES = (".md", ".yaml", ".json", ".jsonl")


@dataclass(frozen=True)
class TextFinding:
    """One path or freshness finding."""

    path: str
    line: int
    kind: str
    text: str


def find_absolute_local_paths(root: Path | None = None, *, paths: list[Path] | None = None) -> list[TextFinding]:
    """Find absolute local machine paths in committed operational docs/records."""

    base = root or repo_root()
    candidates = paths or _tracked_operational_files(base)
    findings: list[TextFinding] = []
    for path in candidates:
        relative = _relative_text(base, path)
        if _skip(relative):
            continue
        example_block = False
        example_fence_seen = False
        for line_no, line in _read_lines(path):
            if "example_path" in line.lower():
                example_block = True
                example_fence_seen = False
                continue
            if example_block and line.strip().startswith("```"):
                if example_fence_seen:
                    example_block = False
                else:
                    example_fence_seen = True
                continue
            if example_block or _line_allows_example_path(line):
                continue
            if any(pattern.search(line) for pattern in LOCAL_PATH_PATTERNS):
                findings.append(TextFinding(relative, line_no, "absolute_local_path", line.strip()))
    return findings


def find_stale_operational_text(root: Path | None = None, *, paths: list[Path] | None = None) -> list[TextFinding]:
    """Find stale current-state phrases in committed operational docs."""

    base = root or repo_root()
    candidates = paths or _stale_doc_files(base)
    findings: list[TextFinding] = []
    for path in candidates:
        relative = _relative_text(base, path)
        if _skip(relative) or not relative.endswith(".md"):
            continue
        for line_no, line in _read_lines(path):
            if any(pattern.search(line) for pattern in STALE_OPERATIONAL_PATTERNS):
                findings.append(TextFinding(relative, line_no, "stale_operational_text", line.strip()))
    return findings


def check_paths_summary(root: Path | None = None) -> dict:
    """Return a concise path/freshness summary."""

    base = root or repo_root()
    path_findings = find_absolute_local_paths(base)
    stale_findings = find_stale_operational_text(base)
    return {
        "absolute_local_path_finding_count": len(path_findings),
        "stale_operational_text_finding_count": len(stale_findings),
        "path_sanitisation_passed": not path_findings and not stale_findings,
        "findings": [finding.__dict__ for finding in [*path_findings, *stale_findings]],
    }


def _tracked_operational_files(root: Path) -> list[Path]:
    names: set[str] = set()
    try:
        result = subprocess.run(
            ["git", "ls-files"],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        )
        names.update(result.stdout.splitlines())
    except (OSError, subprocess.CalledProcessError):
        pass
    for directory in ("data", "docs"):
        base = root / directory
        if base.is_dir():
            names.update(str(path.relative_to(root)).replace("\\", "/") for path in base.rglob("*") if path.is_file())
    names.update(
        name
        for name in (
            "README.md",
            "STATUS.md",
            "ROADMAP.md",
            "AGENTS.md",
            "EXPERIMENTS.md",
            "RESULTS_SCHEMA.md",
            "TESTING.md",
            "CIPHER_CATALOG.md",
        )
        if (root / name).is_file()
    )
    return [
        root / name
        for name in sorted(names)
        if name.startswith(("data/", "docs/"))
        or name in {"README.md", "STATUS.md", "ROADMAP.md", "AGENTS.md", "EXPERIMENTS.md", "RESULTS_SCHEMA.md", "TESTING.md", "CIPHER_CATALOG.md"}
    ]


def _stale_doc_files(root: Path) -> list[Path]:
    names = (
        "README.md",
        "STATUS.md",
        "ROADMAP.md",
        "AGENTS.md",
        "EXPERIMENTS.md",
        "RESULTS_SCHEMA.md",
        "TESTING.md",
        "CIPHER_CATALOG.md",
        "docs/roadmap/staged-plan.md",
        "docs/onboarding/start-here.md",
        "docs/architecture/project-state-and-source-of-truth.md",
        "docs/architecture/project-document-freshness-policy.md",
    )
    return [root / name for name in names if (root / name).is_file()]


def _read_lines(path: Path) -> list[tuple[int, str]]:
    if not path.is_file() or path.suffix.lower() not in OPERATIONAL_SUFFIXES:
        return []
    try:
        return list(enumerate(path.read_text(encoding="utf-8").splitlines(), start=1))
    except UnicodeDecodeError:
        return []


def _relative_text(root: Path, path: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _skip(relative: str) -> bool:
    lower = relative.lower()
    return any(part in lower for part in SKIP_PATH_PARTS)


def _line_allows_example_path(line: str) -> bool:
    lower = line.lower()
    return "example_path" in lower or "example path" in lower or "example command path" in lower
