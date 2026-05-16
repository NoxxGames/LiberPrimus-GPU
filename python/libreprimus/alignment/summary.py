"""Convenience summary helpers for Stage 0D alignment."""

from __future__ import annotations

from pathlib import Path

from libreprimus.alignment.pastebin_to_transcript import align_pastebin_to_transcript
from libreprimus.alignment.models import Stage0DAlignmentSummary


def run_summary(pastebin_path: Path, transcript_path: Path) -> Stage0DAlignmentSummary:
    """Run alignment and return the generated summary."""
    return align_pastebin_to_transcript(pastebin_path, transcript_path)["summary"]
