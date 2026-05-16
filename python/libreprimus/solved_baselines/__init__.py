"""Manifest-addressable solved-baseline runner."""

from __future__ import annotations

from libreprimus.solved_baselines.manifest_loader import load_manifest
from libreprimus.solved_baselines.runner import run_manifest

__all__ = ["load_manifest", "run_manifest"]
