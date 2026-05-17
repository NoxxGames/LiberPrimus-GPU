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
    markdown_path = out_dir / f"{packet.proposal_id}.review.md"
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    markdown_path.write_text(_markdown(packet), encoding="utf-8")
    return {"packet_json": json_path, "review_markdown": markdown_path}


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
        "review_markdown_paths": [packet.generated_output_preview["review_markdown"] for packet in packets],
    }
    path = out_dir / "summary.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def _markdown(packet: ApprovalReadinessPacket) -> str:
    corpus = packet.corpus_slice
    transform_summary = packet.transform_summary
    safety = packet.safety_summary
    metadata_rows = "\n".join(
        "| {label} | `{path}` | {exists} | {role} |".format(
            label=item["label"],
            path=item["path"],
            exists=str(item["exists"]).lower(),
            role=item["role"],
        )
        for item in corpus.get("metadata_paths", [])
    )
    check_rows = "\n".join(
        f"| {item['check']} | {item['result']} | {item['evidence']} | {item['severity']} |"
        for item in packet.machine_check_results
    )
    bound_rows = "\n".join(
        f"| {family} | {count} | bounded preview only; not executed |"
        for family, count in transform_summary.get("candidate_count_by_family", {}).items()
    )
    option_sections = "\n\n".join(
        f"### Option {item['option']}: {item['decision']}\n\n{item['meaning']}\n\n{item['does_not_do']}"
        for item in packet.decision_options
    )
    warnings = "\n".join(f"- {warning}" for warning in packet.warnings) or "- none"
    blocking = "\n".join(f"- {condition}" for condition in packet.blocking_conditions)
    next_commands = "\n".join(f"- `{name}`: {command}" for name, command in packet.next_commands.items())
    return (
        f"# Review packet: {packet.proposal_id}\n\n"
        "## Decision needed\n\n"
        "This proposal is pending. It is not approved and has not executed. "
        "The human decision is approve later execution, revise the proposal, or deny/defer it.\n\n"
        "## Plain-English summary\n\n"
        "This proposal asks whether a later, separately approved CPU-only bounded exploratory run should be prepared "
        "for a reviewable unsolved-material selector. It previews Caesar shifts and affine mod-29 transforms with "
        f"a combined candidate upper bound of `{packet.candidate_count_upper_bound}`. It does not score, use CUDA, "
        "claim a solve, activate the canonical corpus, or finalize page boundaries.\n\n"
        "## Files to inspect\n\n"
        f"- Proposal YAML: `{packet.proposal_path}`\n"
        f"- Pending approval YAML: `{packet.approval_path}`\n"
        f"- Generated JSON packet: `{packet.generated_output_preview['packet_json']}`\n"
        f"- Generated Markdown packet: `{packet.generated_output_preview['review_markdown']}`\n"
        "- Relevant docs: `docs/experiments/first-real-exploratory-proposal.md`\n"
        "- Decision guide: `docs/reference/approval-decision-guide.md`\n\n"
        "## Corpus slice metadata\n\n"
        f"- Slice ID: `{corpus.get('slice_id')}`\n"
        f"- Slice kind: `{corpus.get('slice_kind')}`\n"
        f"- Source: `{corpus.get('source')}`\n"
        f"- Selector: `{json.dumps(corpus.get('selector', {}), sort_keys=True)}`\n"
        f"- Raw unsolved text included: `{str(corpus.get('raw_unsolved_text_included')).lower()}`\n"
        f"- Review required: `{str(corpus.get('review_required')).lower()}`\n\n"
        f"{corpus.get('metadata_path_message')}\n\n"
        "| Metadata item | Path | Exists | Role |\n"
        "| --- | --- | --- | --- |\n"
        f"{metadata_rows}\n\n"
        "## Machine checks\n\n"
        "| Check | Result | Evidence | Severity |\n"
        "| --- | --- | --- | --- |\n"
        f"{check_rows}\n\n"
        "## Candidate bounds\n\n"
        "| Transform family | Count | Notes |\n"
        "| --- | ---: | --- |\n"
        f"{bound_rows}\n"
        f"| total | {transform_summary.get('total_candidate_count')} | upper bound `{transform_summary.get('candidate_count_upper_bound')}` |\n\n"
        "## What approval would allow later\n\n"
        "- A separate future stage could create a scope-bound approval record for this exact proposal SHA.\n"
        "- A later execution stage could evaluate only the explicitly approved bounded Caesar and affine preview scope.\n"
        "- Generated outputs would stay under ignored result paths and still require review.\n\n"
        "## What approval would not allow\n\n"
        "- No CUDA.\n"
        "- No scoring.\n"
        "- No broader search.\n"
        "- No corpus activation.\n"
        "- No solve claim.\n"
        "- No page-boundary finalization.\n\n"
        "## Risks and stop conditions\n\n"
        f"- Recommended decision: `{packet.recommended_decision}`\n"
        f"- Generated outputs ignored: `{str(safety['generated_outputs_ignored']).lower()}`\n"
        f"- Warnings:\n{warnings}\n"
        f"- Blocking conditions:\n{blocking}\n\n"
        "Stop if the reviewer needs a standalone corpus metadata file, narrower selector metadata, tighter transform bounds, "
        "or a different output policy before any approval decision.\n\n"
        "## Decision options\n\n"
        f"{option_sections}\n\n"
        "## Recommended next command\n\n"
        f"{next_commands}\n"
    )


def to_payload(packet: ApprovalReadinessPacket) -> dict[str, Any]:
    return to_jsonable(packet)
