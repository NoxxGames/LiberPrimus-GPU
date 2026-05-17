"""Tiny transparent crib checks for calibration summaries."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any

from libreprimus.paths import repo_root

DEFAULT_CRIBS_PATH = repo_root() / "data/scoring/cribs-tiny-v0.txt"
WORD_RE = re.compile(r"[A-Z]+")


def load_cribs(path: Path = DEFAULT_CRIBS_PATH) -> list[str]:
    resolved = path if path.is_absolute() else repo_root() / path
    return [
        line.strip().upper()
        for line in resolved.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]


def crib_check(
    text: str,
    *,
    candidate_id: str = "inline-text",
    crib_set_id: str = "cribs-tiny-v0",
    cribs: list[str] | None = None,
) -> dict[str, Any]:
    crib_terms = cribs if cribs is not None else load_cribs()
    normalized = " ".join(WORD_RE.findall(text.upper()))
    collapsed = normalized.replace(" ", "")
    hits = sorted({crib for crib in crib_terms if crib and (crib in normalized.split() or crib in collapsed)})
    return {
        "record_type": "crib_check_result",
        "candidate_id": candidate_id,
        "crib_set_id": crib_set_id,
        "crib_hits": hits,
        "crib_hit_count": len(hits),
        "normalized_text_sha256": hashlib.sha256(normalized.encode("utf-8")).hexdigest(),
        "solve_claim": False,
        "notes": ["Crib hits are weak triage features only; not solve evidence."],
    }
