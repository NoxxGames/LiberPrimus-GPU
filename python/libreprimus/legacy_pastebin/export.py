"""High-level extraction and output for legacy Pastebin local TXT sources."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

from libreprimus.legacy_pastebin.infer_anchors import infer_anchors
from libreprimus.legacy_pastebin.loader import load_legacy_pastebin
from libreprimus.legacy_pastebin.models import LegacyPastebinExtraction, to_jsonable
from libreprimus.legacy_pastebin.parser import build_line_pairs
from libreprimus.legacy_pastebin.summary import summarize


def extract_legacy_pastebin(path: Path) -> LegacyPastebinExtraction:
    """Parse, validate, summarize, and infer non-authoritative anchors."""
    loaded = load_legacy_pastebin(path)
    line_pairs, warnings, rune_row_count, prime_value_row_count = build_line_pairs(
        loaded.text,
        loaded.sha256,
    )
    anchors = infer_anchors(line_pairs)
    summary = summarize(
        source_sha256=loaded.sha256,
        line_pairs=line_pairs,
        warnings=warnings,
        rune_row_count=rune_row_count,
        prime_value_row_count=prime_value_row_count,
    )
    return LegacyPastebinExtraction(
        line_pairs=line_pairs,
        anchors=anchors,
        warnings=warnings,
        summary=summary,
    )


def write_json(path: Path, payload: Any) -> None:
    """Write deterministic JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(to_jsonable(payload), indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def write_jsonl(path: Path, records: Iterable[Any]) -> None:
    """Write deterministic JSON Lines."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(to_jsonable(record), sort_keys=True, ensure_ascii=False))
            handle.write("\n")


def write_extraction(out_dir: Path, extraction: LegacyPastebinExtraction) -> dict[str, Path]:
    """Write generated extraction files to an ignored output directory."""
    paths = {
        "line_pairs": out_dir / "line_pairs.jsonl",
        "anchors": out_dir / "anchors.json",
        "summary": out_dir / "summary.json",
        "warnings": out_dir / "warnings.jsonl",
    }
    write_jsonl(paths["line_pairs"], extraction.line_pairs)
    write_json(paths["anchors"], extraction.anchors)
    write_json(paths["summary"], extraction.summary)
    write_jsonl(paths["warnings"], extraction.warnings)
    return paths
