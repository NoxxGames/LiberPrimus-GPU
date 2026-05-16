from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import pytest


REPO = Path(__file__).resolve().parents[2]
REPAIR_SCRIPT = REPO / "scripts" / "ci" / "repair-canonical-json-locks.py"
LOCKED_JSON_FILES = [
    REPO / "data/profiles/gematria/gematria-primus-v0.json",
    REPO / "data/profiles/separators/rtkd-separator-grammar-v0.json",
    REPO / "data/profiles/glyph-variants/glyph-variants-v0.json",
    REPO / "data/transform-registry/cpu-reference-transforms-v0.json",
]


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _lock(path: Path) -> str:
    return path.with_suffix(".sha256").read_text(encoding="utf-8").split()[0]


def _metadata_sha(path: Path) -> str:
    payload = json.loads(path.with_suffix(".metadata.json").read_text(encoding="utf-8"))
    return str(payload["sha256"])


def test_canonical_json_files_have_no_crlf() -> None:
    for path in LOCKED_JSON_FILES:
        assert b"\r\n" not in path.read_bytes(), path


def test_canonical_json_raw_sha_matches_locks() -> None:
    for path in LOCKED_JSON_FILES:
        assert _sha(path) == _lock(path)


def test_metadata_sha_matches_locks() -> None:
    for path in LOCKED_JSON_FILES:
        assert _metadata_sha(path) == _lock(path)


def test_metadata_json_files_have_no_crlf() -> None:
    for path in LOCKED_JSON_FILES:
        assert b"\r\n" not in path.with_suffix(".metadata.json").read_bytes(), path


def test_repair_script_check_passes_without_modifying_files() -> None:
    before = {path: path.read_bytes() for path in LOCKED_JSON_FILES}
    subprocess.run([sys.executable, str(REPAIR_SCRIPT), "--check"], cwd=REPO, check=True)
    after = {path: path.read_bytes() for path in LOCKED_JSON_FILES}
    assert after == before


def test_crlf_json_is_detected_by_repair_helper(tmp_path: Path) -> None:
    spec = importlib.util.spec_from_file_location("repair_canonical_json_locks", REPAIR_SCRIPT)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)

    crlf_path = tmp_path / "crlf.json"
    crlf_path.write_bytes(b'{"ok": true}\r\n')
    with pytest.raises(SystemExit):
        module.verify_no_crlf(crlf_path)
