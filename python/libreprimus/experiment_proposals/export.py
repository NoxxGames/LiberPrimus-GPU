"""Export generated Stage 2G proposal review packets."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from libreprimus.experiment_proposals.models import ReviewPacket
from libreprimus.solved_fixtures.models import to_jsonable


def write_review_packet_outputs(out_dir: Path, packet: ReviewPacket) -> dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = to_jsonable(packet)
    json_path = out_dir / f"{packet.proposal_id}-review-packet.json"
    markdown_path = out_dir / f"{packet.proposal_id}-review-packet.md"
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    markdown_path.write_text(_markdown(packet), encoding="utf-8")
    return {"review_packet_json": json_path, "review_packet_markdown": markdown_path}


def write_summary(out_dir: Path, packets: list[ReviewPacket]) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    payload: dict[str, Any] = {
        "record_type": "experiment_review_packet_summary",
        "packet_count": len(packets),
        "proposal_ids": [packet.proposal_id for packet in packets],
        "blocked_count": sum(1 for packet in packets if packet.execution_blocked),
        "approved_count": sum(1 for packet in packets if packet.approved_for_execution),
        "pending_or_missing_count": sum(
            1 for packet in packets if packet.approval_status in {"pending", "missing"}
        ),
        "denied_count": sum(1 for packet in packets if packet.approval_status == "denied"),
        "candidate_plaintexts_included": False,
    }
    path = out_dir / "summary.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def _markdown(packet: ReviewPacket) -> str:
    return (
        f"# Review Packet: {packet.proposal_id}\n\n"
        f"- Approval status: `{packet.approval_status}`\n"
        f"- Approved for execution: `{str(packet.approved_for_execution).lower()}`\n"
        f"- Execution blocked: `{str(packet.execution_blocked).lower()}`\n"
        f"- Candidate count estimate: `{packet.proposal_summary['candidate_count_estimate']}`\n"
        f"- Candidate count upper bound: `{packet.proposal_summary['candidate_count_upper_bound']}`\n\n"
        "No candidate plaintexts are included in this review packet.\n"
    )

