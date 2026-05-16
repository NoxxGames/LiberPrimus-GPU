from pathlib import Path

from libreprimus.alignment.pastebin_to_transcript import align_pastebin_to_transcript_followup

S = "\u16cb"
H = "\u16bb"
F = "\u16a0"


def _write(path: Path, text: str) -> Path:
    path.write_text(text, encoding="utf-8")
    return path


def test_gap_summary_classifies_no_match_and_empty_pair(tmp_path: Path) -> None:
    pastebin = _write(tmp_path / "pastebin.txt", f"{{{S}{H}}}\n{{{{53,23}}}}\n{{}}\n{{}}\n")
    transcript = _write(tmp_path / "rtkd.txt", f"{F}/\n")

    result = align_pastebin_to_transcript_followup(pastebin, transcript)

    gap_summary = result["gap_summary"]
    assert gap_summary.total_pairs == 2
    assert gap_summary.no_match_pairs >= 1
    assert gap_summary.empty_pair_count == 1
    assert gap_summary.gap_reason_counts["empty_pair"] == 1
    assert gap_summary.unresolved_pairs >= 1


def test_gap_diagnostics_include_signature_fields(tmp_path: Path) -> None:
    pastebin = _write(tmp_path / "pastebin.txt", f"{{{S}{H}}}\n{{{{53,23}}}}\n")
    transcript = _write(tmp_path / "rtkd.txt", f"{F}/\n")

    result = align_pastebin_to_transcript_followup(pastebin, transcript)
    diagnostic = result["gap_diagnostics"][0]

    assert diagnostic.record_type == "alignment_gap_diagnostic"
    assert diagnostic.flattened_rune_sha256
    assert diagnostic.normalized_rune_sha256
    assert diagnostic.decimal_index_sha256
    assert diagnostic.trusted_as_canonical is False
