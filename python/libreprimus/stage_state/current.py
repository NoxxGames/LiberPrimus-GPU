"""Loader for the project current-stage registry."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from libreprimus.validation.stage_id import stage_display_label, stage_command_suffix

CURRENT_STAGE_STATE_PATH = Path("data/project-state/current-stage-state.yaml")


def load_current_stage_state(path: Path = CURRENT_STAGE_STATE_PATH) -> dict[str, Any]:
    if not path.exists():
        return {}
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return payload if isinstance(payload, dict) else {}


def current_latest_stage_id(path: Path = CURRENT_STAGE_STATE_PATH) -> str:
    state = load_current_stage_state(path)
    return str(state.get("latest_completed_stage_id") or "")


def current_next_stage_id(path: Path = CURRENT_STAGE_STATE_PATH) -> str:
    state = load_current_stage_state(path)
    return str(state.get("recommended_next_stage_id") or "")


def current_latest_stage_label(path: Path = CURRENT_STAGE_STATE_PATH) -> str:
    latest = current_latest_stage_id(path)
    return stage_display_label(latest) if latest else ""


def current_next_stage_label(path: Path = CURRENT_STAGE_STATE_PATH) -> str:
    next_stage = current_next_stage_id(path)
    return stage_display_label(next_stage) if next_stage else ""


def current_latest_stage_command_suffix(path: Path = CURRENT_STAGE_STATE_PATH) -> str:
    latest = current_latest_stage_id(path)
    return stage_command_suffix(latest) if latest else ""
