"""Best-effort toolchain detection that does not run stego/audio extraction."""

from __future__ import annotations

import shutil
from typing import Any

from libreprimus.stego_positive_controls.models import COMMON_FALSE_FLAGS


def detect_toolchains() -> list[dict[str, Any]]:
    """Detect known tools by path only."""

    return [
        _record("outguess", "outguess", missing_state="outguess_missing", available_state="outguess_available_unverified"),
        _record("openpuff", "openpuff", missing_state="openpuff_manual_required", available_state="openpuff_manual_required"),
        _record("mp3stego", "mp3stego", missing_state="mp3stego_manual_required", available_state="mp3stego_manual_required"),
        _record("hexdump/strings", "strings", missing_state="missing", available_state="hexdump_strings_available"),
        _record("certutil", "certutil", missing_state="missing", available_state="not_applicable"),
        {
            "record_type": "stego_toolchain_readiness",
            "toolchain_record_id": "stage4n-toolchain-audio-rendering",
            "toolchain": "audio_rendering",
            "toolchain_state": "not_applicable",
            "available": False,
            "tool_path": None,
            "tool_help_sha256": None,
            "notes": "Audio rendering is not required for Stage 4N readiness metadata.",
            **COMMON_FALSE_FLAGS,
        },
        {
            "record_type": "stego_toolchain_readiness",
            "toolchain_record_id": "stage4n-toolchain-synthetic-control",
            "toolchain": "synthetic_control",
            "toolchain_state": "audio_tools_not_required",
            "available": True,
            "tool_path": None,
            "tool_help_sha256": None,
            "notes": "Synthetic controls use deterministic metadata and do not require historical stego tools.",
            **COMMON_FALSE_FLAGS,
        },
    ]


def _record(toolchain: str, command: str, *, missing_state: str, available_state: str) -> dict[str, Any]:
    path = shutil.which(command)
    return {
        "record_type": "stego_toolchain_readiness",
        "toolchain_record_id": f"stage4n-toolchain-{toolchain.replace('/', '-').replace(' ', '-')}",
        "toolchain": toolchain,
        "toolchain_state": available_state if path else missing_state,
        "available": bool(path),
        "tool_path": "available_on_path" if path else None,
        "tool_help_sha256": None,
        "notes": "Path detection only; Stage 4N does not execute extraction tools.",
        **COMMON_FALSE_FLAGS,
    }
