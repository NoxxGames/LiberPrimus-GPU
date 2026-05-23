"""Research-bundle scaffold builder."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .export import read_records, repo_relative, resolve, write_json
from .models import RESEARCH_BUNDLE_PLAN_REPORT, REQUIRED_BUNDLE_IDS
from .policy import require_safe_output_root


def build_bundle_scaffolds(*, bundle_plan_path: Path, out_root: Path) -> list[dict[str, Any]]:
    """Create ignored local research-bundle preview scaffolds."""

    require_safe_output_root(out_root)
    records = read_records(bundle_plan_path)
    missing = REQUIRED_BUNDLE_IDS.difference(record["bundle_id"] for record in records)
    if missing:
        raise ValueError(f"bundle plan missing required bundle IDs: {sorted(missing)}")
    root = resolve(out_root)
    root.mkdir(parents=True, exist_ok=True)
    built: list[dict[str, Any]] = []
    for record in sorted(records, key=lambda item: item["recommended_deep_research_order"]):
        bundle_dir = root / record["bundle_id"]
        bundle_dir.mkdir(parents=True, exist_ok=True)
        (bundle_dir / "do_not_assume.md").write_text(
            _do_not_assume_text(record),
            encoding="utf-8",
        )
        (bundle_dir / "known_questions.md").write_text(_known_questions_text(record), encoding="utf-8")
        (bundle_dir / "source_ids.txt").write_text(
            "\n".join(record.get("included_source_ids", [])) + "\n",
            encoding="utf-8",
        )
        (bundle_dir / "bundle_manifest.json").write_text(
            json.dumps(record, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        built.append(
            {
                "bundle_id": record["bundle_id"],
                "bundle_path": repo_relative(bundle_dir),
                "do_not_assume_generated": True,
                "known_questions_generated": True,
                "ready_after_stage5af": bool(record.get("ready_after_stage5af")),
            }
        )
    write_json(root.parent / RESEARCH_BUNDLE_PLAN_REPORT, {"records": built})
    return built


def _do_not_assume_text(record: dict[str, Any]) -> str:
    lines = [
        f"# {record['title']}",
        "",
        "Do not assume:",
    ]
    notes = record.get("do_not_assume_notes", [])
    lines.extend(f"- {note}" for note in notes)
    lines.extend(
        [
            "- Source-lock/provenance inventory is not hypothesis execution.",
            "- Generated bundle previews remain ignored local material.",
            "",
        ]
    )
    return "\n".join(lines)


def _known_questions_text(record: dict[str, Any]) -> str:
    lines = [
        f"# {record['title']} Known Questions",
        "",
        f"Purpose: {record.get('purpose', '')}",
        "",
        "Required manual inputs:",
    ]
    manual_inputs = record.get("required_manual_inputs", [])
    if manual_inputs:
        lines.extend(f"- {item}" for item in manual_inputs)
    else:
        lines.append("- None identified for the dry-run scaffold.")
    lines.extend(["", "Sequential order:", f"- {record.get('recommended_deep_research_order')}", ""])
    return "\n".join(lines)
