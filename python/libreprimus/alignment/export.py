"""Export helpers for Stage 0D generated alignment records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

from libreprimus.legacy_pastebin.models import to_jsonable


def write_json(path: Path, payload: Any) -> None:
    """Write deterministic JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(to_jsonable(payload), indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def write_jsonl(path: Path, records: Iterable[Any]) -> None:
    """Write deterministic JSONL."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(to_jsonable(record), sort_keys=True, ensure_ascii=False))
            handle.write("\n")


def write_stage0d_outputs(out_dir: Path, result: dict[str, Any]) -> dict[str, Path]:
    """Write generated Stage 0D outputs to an ignored directory."""
    paths = {
        "transcript_lines": out_dir / "transcript_lines.jsonl",
        "pastebin_alignment": out_dir / "pastebin_alignment.jsonl",
        "page_boundary_candidates": out_dir / "page_boundary_candidates.jsonl",
        "glyph_variant_observations": out_dir / "glyph_variant_observations.jsonl",
        "alignment_summary": out_dir / "alignment_summary.json",
        "warnings": out_dir / "warnings.jsonl",
    }
    write_jsonl(paths["transcript_lines"], result["transcript_records"])
    write_jsonl(paths["pastebin_alignment"], result["alignments"])
    write_jsonl(paths["page_boundary_candidates"], result["boundary_candidates"])
    write_jsonl(paths["glyph_variant_observations"], result["glyph_variant_observations"])
    write_json(paths["alignment_summary"], result["summary"])
    write_jsonl(paths["warnings"], result["summary"].warnings)
    return paths
