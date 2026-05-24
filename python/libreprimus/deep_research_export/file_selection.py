"""Stage 5AN file-selection policy."""

from __future__ import annotations

import re
from pathlib import Path

from .inputs import repo_relative, resolve
from .models import ALLOWED_PRIVATE_EXTENSIONS, FORBIDDEN_RAW_EXTENSIONS

ABSOLUTE_PATH_PATTERNS = [
    re.compile(r"\b[A-Za-z]:[\\/][^\s\"'<>]+"),
    re.compile(r"\\\\[A-Za-z0-9_.-]+\\[^\s\"'<>]+"),
    re.compile(r"/home/[^\s\"'<>]+"),
    re.compile(r"/mnt/[^\s\"'<>]+"),
    re.compile(r"/Users/[^\s\"'<>]+"),
]
PRIVATE_ID_PATTERNS = [
    re.compile(r"cdn\.discordapp\.com/attachments/[^\s\"'<>]+", re.IGNORECASE),
    re.compile(r"discord(?:app)?\.com/channels/\d{12,}[^\s\"'<>]*", re.IGNORECASE),
    re.compile(r"(token|session|cookie|auth)[=:][A-Za-z0-9_.-]{12,}", re.IGNORECASE),
]


def is_allowed_private_file(path: Path) -> bool:
    """Return true when a generated private input file can be copied."""

    return path.suffix.lower() in ALLOWED_PRIVATE_EXTENSIONS and path.name != ".gitkeep"


def is_forbidden_raw_file(path: Path) -> bool:
    """Return true when a file is raw/binary and excluded by default."""

    lowered = path.name.lower()
    if lowered in {"thumbs.db", ".ds_store"}:
        return True
    return path.suffix.lower() in FORBIDDEN_RAW_EXTENSIONS


def slugify(value: str) -> str:
    """Return a stable filesystem slug."""

    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-._").lower()
    return slug or "item"


def sanitize_text(text: str) -> tuple[str, list[str]]:
    """Redact local paths and private identifiers with explicit finding labels."""

    findings: list[str] = []
    sanitized = text
    for pattern in ABSOLUTE_PATH_PATTERNS:
        if pattern.search(sanitized):
            findings.append("local_absolute_path_redacted")
            sanitized = pattern.sub("[redacted-local-path]", sanitized)
    for pattern in PRIVATE_ID_PATTERNS:
        if pattern.search(sanitized):
            findings.append("private_identifier_redacted")
            sanitized = pattern.sub("[redacted-private-reference]", sanitized)
    return sanitized, sorted(set(findings))


def select_research_input_files(roots: list[Path]) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    """Select generated/private research-input files and record excluded paths."""

    selected: list[dict[str, str]] = []
    excluded: list[dict[str, str]] = []
    for root_path in roots:
        root = resolve(root_path)
        if not root.exists():
            excluded.append({"path": repo_relative(root_path), "reason": "input_root_missing"})
            continue
        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            rel = repo_relative(path)
            if is_allowed_private_file(path):
                selected.append(
                    {
                        "source_path": rel,
                        "path_kind": "generated_private_research_input",
                        "publication_status": "private_deep_research_only",
                        "review_status": "review_required",
                        "raw_source_origin": "research_inputs",
                    }
                )
            elif is_forbidden_raw_file(path):
                excluded.append({"path": rel, "reason": "forbidden_raw_or_binary_extension"})
            else:
                excluded.append({"path": rel, "reason": "extension_not_in_private_content_policy"})
    return selected, excluded
