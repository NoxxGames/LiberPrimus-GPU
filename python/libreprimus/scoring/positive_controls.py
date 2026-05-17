"""Positive-control text loading from committed solved fixtures."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from libreprimus.paths import repo_root

DEFAULT_FIXTURE_DIRS = [
    repo_root() / "data/fixtures/solved-pages/direct-translation-v0",
    repo_root() / "data/fixtures/solved-pages/atbash-family-v0",
    repo_root() / "data/fixtures/solved-pages/vigenere-v0",
    repo_root() / "data/fixtures/solved-pages/prime-stream-v0",
]

SYNTHETIC_POSITIVE_CONTROLS = [
    {
        "control_id": "synthetic-readable-control-001",
        "source": "synthetic_readable_control",
        "method_family": "synthetic",
        "text": "THE PATH OF WISDOM IS TO KNOW THE SELF.",
    },
    {
        "control_id": "synthetic-readable-control-002",
        "source": "synthetic_readable_control",
        "method_family": "synthetic",
        "text": "LIBER PRIMUS IS A QUESTION AND AN ANSWER.",
    },
]


def load_positive_control_texts(fixture_dirs: list[Path] | None = None) -> list[dict[str, Any]]:
    controls: list[dict[str, Any]] = []
    dirs = fixture_dirs if fixture_dirs is not None else DEFAULT_FIXTURE_DIRS
    for fixture_dir in dirs:
        resolved = fixture_dir if fixture_dir.is_absolute() else repo_root() / fixture_dir
        for path in sorted(resolved.glob("*.fixture.json")):
            payload = json.loads(path.read_text(encoding="utf-8"))
            text = payload.get("expected_normalized_plaintext")
            if not isinstance(text, str) or not text.strip():
                continue
            fixture_id = str(payload.get("fixture_id", path.stem))
            method_family = str(payload.get("method_family", "unknown"))
            controls.append(
                {
                    "control_id": f"positive-{fixture_id}",
                    "source": str(path.relative_to(repo_root())),
                    "method_family": method_family,
                    "text": text,
                }
            )
    controls.extend(SYNTHETIC_POSITIVE_CONTROLS)
    return controls
