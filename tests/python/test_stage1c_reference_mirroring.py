import json
import subprocess
from pathlib import Path

import pytest

from libreprimus.reference_sources.scream314_pages_and_ciphers import extract_method_notes
from libreprimus.reference_sources.summary import build_stage1c_reference_summary


def test_reference_lock_metadata_policy_flags() -> None:
    path = Path("data/locks/reference-repos/reference-source-mirror-stage-1c.metadata.json")
    payload = json.loads(path.read_text(encoding="utf-8"))

    assert payload["reference_only"] is True
    assert payload["imported_as_dependency"] is False
    assert payload["code_copied"] is False


def test_raw_mirrored_files_are_ignored() -> None:
    result = subprocess.run(
        [
            "git",
            "check-ignore",
            "-q",
            "data/raw/reference-repos/scream314-cicada3301/pages_and_ciphers.md",
        ],
        check=False,
    )

    assert result.returncode == 0


def test_synthetic_scream314_extraction_detects_vigenere_keys_and_skip(tmp_path: Path) -> None:
    path = tmp_path / "pages_and_ciphers.md"
    path.write_text(
        "03.jpg-04.jpg DIVINITY Shift up forward Gematria. "
        "Note: Every clear text F is an F, and needs to be skipped.\n"
        "14.jpg-15.jpg FIRFUMFERENFE Shift up forward Gematria.\n",
        encoding="utf-8",
    )

    notes = extract_method_notes(path)

    assert any(note.key_candidate == "DIVINITY" for note in notes)
    assert any(note.key_candidate == "FIRFUMFERENFE" for note in notes)
    assert any(note.skip_rule_candidate == "cleartext_f_pass_through" for note in notes)


def test_stage1c_reference_summary_detects_local_notes() -> None:
    if not Path("data/raw/reference-repos/scream314-cicada3301/pages_and_ciphers.md").is_file():
        pytest.skip("local mirrored reference sources are ignored and absent in raw-data-free CI")

    summary = build_stage1c_reference_summary()["summary"]

    assert summary["reference_only"] is True
    assert summary["divinity_found"] is True
    assert summary["firfumferenfe_found"] is True
    assert summary["cleartext_f_skip_note_found"] is True
    assert summary["imported_as_dependency"] is False
    assert summary["code_copied"] is False
