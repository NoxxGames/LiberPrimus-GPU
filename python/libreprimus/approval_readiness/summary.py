"""Load generated Stage 2I approval-readiness summaries."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_summary(results_dir: Path) -> dict[str, Any]:
    path = results_dir / "summary.json"
    if not path.is_file():
        return {
            "record_type": "approval_readiness_summary",
            "packet_count": 0,
            "proposal_count": 0,
            "pending_count": 0,
            "approved_count": 0,
            "candidate_count_estimate_total": 0,
            "blocking_condition_count": 0,
        }
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Approval-readiness summary must be a JSON object: {path}")
    return payload


def load_packets(results_dir: Path) -> list[dict[str, Any]]:
    packets = []
    for path in sorted(results_dir.glob("*-approval-readiness-packet.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError(f"Approval-readiness packet must be a JSON object: {path}")
        packets.append(payload)
    return packets
