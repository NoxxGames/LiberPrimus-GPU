"""Stage identifier normalization for validation wrappers."""

from __future__ import annotations

import re


def normalize_stage_token(value: str) -> str:
    """Return a compact command-safe stage token such as ``stage5ea``."""
    token = re.sub(r"[^a-zA-Z0-9]", "", value).lower()
    if not token:
        raise ValueError("stage identifier is empty")
    if token.startswith("stage"):
        return token
    if token.isalpha():
        return f"stage5{token}"
    return f"stage{token}"


def stage_command_suffix(value: str) -> str:
    return normalize_stage_token(value)


def validation_command_name(value: str) -> str:
    return f"validate-{stage_command_suffix(value)}"


def stage_display_label(value: str) -> str:
    token = normalize_stage_token(value)
    suffix = token.removeprefix("stage").upper()
    return f"Stage {suffix}"
