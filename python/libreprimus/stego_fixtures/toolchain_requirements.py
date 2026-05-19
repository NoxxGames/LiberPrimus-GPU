"""Toolchain requirement records for future stego/audio fixture work."""

from __future__ import annotations

from typing import Any


def build_toolchain_requirements() -> list[dict[str, Any]]:
    """Return Stage 4F toolchain requirement records."""

    return [
        _requirement("stage4f-toolchain-outguess", "outguess", ["outguess positive/negative matrix"]),
        _requirement("stage4f-toolchain-openpuff", "openpuff", ["Interconnectedness fixture preparation"]),
        _requirement("stage4f-toolchain-mp3stego", "mp3stego", ["MP3/Instar deterministic regression prep"]),
        _requirement("stage4f-toolchain-hexdump-strings", "hexdump/strings", ["audio hexdump/string baseline"]),
        _requirement("stage4f-toolchain-audio-rendering", "audio_rendering", ["audio fixture metadata review"]),
    ]


def _requirement(requirement_id: str, toolchain: str, required_for: list[str]) -> dict[str, Any]:
    return {
        "record_type": "toolchain_requirement_record",
        "requirement_id": requirement_id,
        "toolchain": toolchain,
        "required_for": required_for,
        "execution_status": "not_executed_stage4f",
        "raw_file_committed": False,
        "binary_committed": False,
        "audio_committed": False,
        "image_committed": False,
        "extracted_payload_committed": False,
        "font_committed": False,
        "trusted_as_canonical": False,
        "solve_claim": False,
        "notes": "Requirement recorded only; Stage 4F does not run this toolchain.",
    }
