"""Stage 1C reference-source summary generation."""

from __future__ import annotations

from pathlib import Path
from time import perf_counter
from typing import Any

from libreprimus.paths import repo_root
from libreprimus.reference_sources.export import write_json, write_jsonl
from libreprimus.reference_sources.lipeeeee_gematria_reference import extract_tooling_notes
from libreprimus.reference_sources.scream314_pages_and_ciphers import extract_method_notes

DEFAULT_STAGE1C_REFERENCE_OUT_DIR = Path("data/normalized/reference-summaries/stage-1c")
DEFAULT_SCREAM314_PAGES_AND_CIPHERS = Path(
    "data/raw/reference-repos/scream314-cicada3301/pages_and_ciphers.md"
)
DEFAULT_LIPEEEEE_ROOT = Path("data/raw/reference-repos/lipeeeee-gematria")


def build_stage1c_reference_summary(
    *,
    pages_and_ciphers_path: Path | None = None,
    lipeeeee_root: Path | None = None,
) -> dict[str, Any]:
    start = perf_counter()
    root = repo_root()
    pages_path = pages_and_ciphers_path or root / DEFAULT_SCREAM314_PAGES_AND_CIPHERS
    lipeeeee_path = lipeeeee_root or root / DEFAULT_LIPEEEEE_ROOT
    method_notes = extract_method_notes(pages_path) if pages_path.is_file() else []
    tooling_notes = extract_tooling_notes(lipeeeee_path) if lipeeeee_path.is_dir() else []
    summary = {
        "record_type": "stage1c_reference_source_summary",
        "reference_only": True,
        "imported_as_dependency": False,
        "code_copied": False,
        "scream314_method_note_count": len(method_notes),
        "lipeeeee_tooling_note_count": len(tooling_notes),
        "divinity_found": any(note.key_candidate == "DIVINITY" for note in method_notes),
        "firfumferenfe_found": any(note.key_candidate == "FIRFUMFERENFE" for note in method_notes),
        "cleartext_f_skip_note_found": any(
            note.skip_rule_candidate == "cleartext_f_pass_through" for note in method_notes
        ),
        "elapsed_ms": round((perf_counter() - start) * 1000, 3),
    }
    return {"method_notes": method_notes, "tooling_notes": tooling_notes, "summary": summary}


def write_stage1c_reference_outputs(out_dir: Path, payload: dict[str, Any]) -> dict[str, Path]:
    paths = {
        "reference_method_notes": out_dir / "reference_method_notes.jsonl",
        "tooling_reference_notes": out_dir / "tooling_reference_notes.jsonl",
        "summary": out_dir / "summary.json",
    }
    write_jsonl(paths["reference_method_notes"], payload["method_notes"])
    write_jsonl(paths["tooling_reference_notes"], payload["tooling_notes"])
    write_json(paths["summary"], payload["summary"])
    return paths
