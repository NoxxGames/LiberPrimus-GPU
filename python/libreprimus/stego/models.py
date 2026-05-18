"""Models for Stage 3V OutGuess regression."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class StegoArtifact:
    """Committed metadata for one stego regression artefact."""

    artifact_id: str
    expected_role: str
    local_path: Path
    local_path_status: str
    expected_payload_sha256: str | None
    media_type: str
    payload: dict[str, Any]


@dataclass(frozen=True)
class OutGuessCase:
    """One manifest case."""

    case_id: str
    artifact_id: str
    enabled: bool
    expected_role: str
    generate_synthetic: str | None
    require_expected_payload_hash: bool
    notes: str
    payload: dict[str, Any]


@dataclass(frozen=True)
class OutGuessManifest:
    """Validated OutGuess regression manifest."""

    manifest_id: str
    allow_missing_tool: bool
    allow_missing_assets: bool
    cases: tuple[OutGuessCase, ...]
    expected_case_count_upper_bound: int
    payload: dict[str, Any]


@dataclass(frozen=True)
class OutGuessTool:
    """Detected OutGuess tool metadata."""

    available: bool
    path: Path | None
    help_output_sha256: str | None
    help_output: str
    notes: str
