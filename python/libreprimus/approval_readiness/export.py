"""Export generated Stage 2I approval-readiness packets."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from libreprimus.approval_readiness.models import ApprovalReadinessPacket
from libreprimus.approval_readiness.validation import validate_record
from libreprimus.solved_fixtures.models import to_jsonable


def write_approval_readiness_outputs(out_dir: Path, packet: ApprovalReadinessPacket) -> dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = validate_record(packet)
    json_path = out_dir / f"{packet.proposal_id}-approval-readiness-packet.json"
    markdown_path = out_dir / f"{packet.proposal_id}-approval-readiness-packet.md"
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    markdown_path.write_text(_markdown(packet), encoding="utf-8")
    return {"packet_json": json_path, "packet_markdown": markdown_path}


def write_summary(out_dir: Path, packets: list[ApprovalReadinessPacket]) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    payload: dict[str, Any] = {
        "record_type": "approval_readiness_summary",
        "packet_count": len(packets),
        "proposal_count": len({packet.proposal_id for packet in packets}),
        "pending_count": sum(1 for packet in packets if packet.approval_status == "pending"),
        "approved_count": sum(1 for packet in packets if packet.approval_status == "approved"),
        "candidate_count_estimate_total": sum(packet.candidate_count_estimate for packet in packets),
        "blocking_condition_count": sum(len(packet.blocking_conditions) for packet in packets),
        "candidate_outputs_included": False,
    }
    path = out_dir / "summary.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def _markdown(packet: ApprovalReadinessPacket) -> str:
    return (
        f"# Approval Readiness Packet: {packet.proposal_id}\n\n"
        f"- Approval status: `{packet.approval_status}`\n"
        f"- Approved for execution: `{str(packet.approved_for_execution).lower()}`\n"
        f"- Execution enabled: `{str(packet.execution_enabled).lower()}`\n"
        f"- Candidate count estimate: `{packet.candidate_count_estimate}`\n"
        f"- Candidate count upper bound: `{packet.candidate_count_upper_bound}`\n"
        f"- Blocking conditions: `{len(packet.blocking_conditions)}`\n\n"
        "No raw unsolved text, candidate plaintexts, scoring output, execution output, or CUDA output is included.\n"
    )


def to_payload(packet: ApprovalReadinessPacket) -> dict[str, Any]:
    return to_jsonable(packet)
