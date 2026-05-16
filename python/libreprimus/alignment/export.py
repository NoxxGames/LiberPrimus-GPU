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


def write_stage0d_followup_outputs(out_dir: Path, result: dict[str, Any]) -> dict[str, Path]:
    """Write generated Stage 0D-followup outputs to an ignored directory."""
    paths = {
        "transcript_lines": out_dir / "transcript_lines.jsonl",
        "transcript_views_summary": out_dir / "transcript_views_summary.json",
        "pastebin_alignment": out_dir / "pastebin_alignment.jsonl",
        "alignment_gap_diagnostics": out_dir / "alignment_gap_diagnostics.jsonl",
        "alignment_gap_summary": out_dir / "alignment_gap_summary.json",
        "page_boundary_candidates": out_dir / "page_boundary_candidates.jsonl",
        "page_boundary_audit": out_dir / "page_boundary_audit.json",
        "page_boundary_confidence_audit": out_dir / "page_boundary_confidence_audit.jsonl",
        "glyph_variant_observations": out_dir / "glyph_variant_observations.jsonl",
        "alignment_summary": out_dir / "alignment_summary.json",
        "warnings": out_dir / "warnings.jsonl",
    }
    write_jsonl(paths["transcript_lines"], result["transcript_records"])
    if result.get("transcript_views_summary") is not None:
        write_json(paths["transcript_views_summary"], result["transcript_views_summary"])
    else:
        write_json(paths["transcript_views_summary"], {})
    write_jsonl(paths["pastebin_alignment"], result["alignments"])
    write_jsonl(paths["alignment_gap_diagnostics"], result.get("gap_diagnostics", []))
    write_json(paths["alignment_gap_summary"], result.get("gap_summary", {}))
    write_jsonl(paths["page_boundary_candidates"], result["boundary_candidates"])
    write_json(paths["page_boundary_audit"], result.get("boundary_audit_summary", {}))
    write_jsonl(paths["page_boundary_confidence_audit"], result.get("boundary_audits", []))
    write_jsonl(paths["glyph_variant_observations"], result["glyph_variant_observations"])
    write_json(paths["alignment_summary"], result["summary"])
    warnings = []
    summary = result.get("summary")
    if hasattr(summary, "warnings"):
        warnings.extend(summary.warnings)
    for alignment in result.get("alignments", []):
        warnings.extend(getattr(alignment, "warnings", []))
    write_jsonl(paths["warnings"], warnings)
    return paths
