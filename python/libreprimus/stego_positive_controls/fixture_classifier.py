"""Classify committed fixture metadata into Stage 4N readiness categories."""

from __future__ import annotations

from typing import Any


def classify_outguess_fixture(record: dict[str, Any]) -> str:
    """Return the Stage 4N outguess fixture category for a committed record."""

    artifact_type = str(record.get("artifact_type") or "").lower()
    expected_role = str(record.get("expected_role") or "").lower()
    fixture_id = str(record.get("fixture_id") or record.get("artifact_id") or "").lower()
    source_path = str(record.get("source_path") or record.get("local_path") or "").lower()
    if "synthetic" in fixture_id or str(record.get("source_class") or "") == "synthetic_control":
        return "synthetic_positive_control" if "positive" in expected_role or "positive" in fixture_id else "synthetic_negative_control"
    if artifact_type == "lp_outguessed" or "lp_outguessed" in source_path:
        return "lp_outguessed_reference"
    if artifact_type == "image_fixture_candidate" or source_path.endswith((".jpg", ".jpeg", ".png")):
        return "image_fixture_candidate"
    if "negative" in expected_role:
        return "outguess_known_negative_candidate"
    if "positive" in expected_role:
        return "outguess_known_positive_candidate"
    if artifact_type == "reference_source":
        return "outguess_reference_only"
    return "outguess_reference_only"


def classify_audio_fixture(record: dict[str, Any]) -> str:
    """Return the Stage 4N audio fixture category for a committed record."""

    fixture_id = str(record.get("fixture_id") or "").lower()
    source_path = str(record.get("source_path") or "").lower()
    toolchain = {str(item).lower() for item in record.get("toolchain", []) if item is not None}
    artifact_type = str(record.get("artifact_type") or "").lower()
    if "interconnectedness" in fixture_id or "interconnectedness" in source_path:
        return "openpuff_interconnectedness_candidate"
    if "761" in fixture_id or "761" in source_path or "instar" in fixture_id or "instar" in source_path:
        return "mp3_instar_candidate"
    if "hexdump/strings" in toolchain:
        return "audio_hexdump_candidate"
    if artifact_type == "reference_source":
        return "outguess_reference_only"
    return "audio_hexdump_candidate"
