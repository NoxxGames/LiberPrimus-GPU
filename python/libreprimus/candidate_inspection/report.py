"""Write Stage 3B inspection and rerank reports."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from libreprimus.candidate_inspection.models import InspectionSummary
from libreprimus.paths import repo_root
from libreprimus.solved_fixtures.models import to_jsonable


def resolve_output_path(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path


def write_inspection_markdown(path: Path, summary: InspectionSummary) -> Path:
    resolved = resolve_output_path(path)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    top = summary.top_candidate
    refined = summary.refined_top_candidate or {}
    lines = [
        "# Stage 3B Stage 3A Lead Inspection",
        "",
        f"Run ID: `{summary.run_id}`",
        f"Candidate count inspected: `{summary.candidate_count}`",
        f"Top-N inspected: `{summary.top_n}`",
        "",
        "## Original Top Lead",
        "",
        f"- Candidate index: `{top.get('candidate_index')}`",
        f"- Transform family: `{top.get('transform_family')}`",
        f"- Transform parameters: `{json.dumps(top.get('transform_parameters', {}), sort_keys=True)}`",
        f"- Total score: `{top.get('total_score')}`",
        f"- Output SHA-256: `{top.get('output_sha256')}`",
        f"- Vowel ratio: `{top.get('vowel_ratio')}`",
        f"- Common word hits: `{', '.join(top.get('common_word_hits', [])) or 'none'}`",
        f"- Separator-aware word count: `{top.get('separator_aware_word_count')}`",
        f"- Negative features: `{', '.join(top.get('negative_features', [])) or 'none recorded in original score'}`",
        "",
        "## Refined Top Lead",
        "",
        f"- Candidate index: `{refined.get('candidate_index', 'not reranked')}`",
        f"- Transform family: `{refined.get('transform_family', 'not reranked')}`",
        f"- Transform parameters: `{json.dumps(refined.get('transform_parameters', {}), sort_keys=True)}`",
        f"- Total score: `{refined.get('total_score', 'not reranked')}`",
        f"- Length-normalized score: `{refined.get('length_normalized_score', 'not reranked')}`",
        f"- Confidence label: `{refined.get('confidence_label', 'not reranked')}`",
        "",
        "## Score Distribution",
        "",
        f"- Min: `{summary.score_distribution['min']}`",
        f"- Median: `{summary.score_distribution['median']}`",
        f"- Mean: `{summary.score_distribution['mean']}`",
        f"- Max: `{summary.score_distribution['max']}`",
        f"- Top1 minus top2: `{summary.score_gaps['top1_minus_top2']}`",
        f"- Top1 minus top10: `{summary.score_gaps['top1_minus_top10']}`",
        "",
        "## Transform Family Counts",
        "",
        f"- All candidates: `{json.dumps(summary.transform_family_counts, sort_keys=True)}`",
        f"- Top candidates: `{json.dumps(summary.top_transform_family_counts, sort_keys=True)}`",
        "",
        "## Inspection Result",
        "",
        f"- Qualitative label: `{summary.qualitative_label}`",
        f"- Recommendation: {summary.recommendation}",
        "- Solve claim: false",
        "- CUDA used: false",
        "- Full candidate dump committed: false",
        "",
        "## Warnings",
        "",
    ]
    lines.extend(f"- `{warning}`" for warning in summary.warnings)
    if not summary.warnings:
        lines.append("- none")
    resolved.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return resolved


def write_json(path: Path, payload: Any) -> Path:
    resolved = resolve_output_path(path)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    resolved.write_text(json.dumps(to_jsonable(payload), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return resolved


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> Path:
    resolved = resolve_output_path(path)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    with resolved.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(to_jsonable(record), sort_keys=True))
            handle.write("\n")
    return resolved
