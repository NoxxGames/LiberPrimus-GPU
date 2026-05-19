"""Stage 4E source-delta audit orchestration."""

from __future__ import annotations

from pathlib import Path
from typing import Any
import json

from libreprimus.source_delta_audit.disabled_manifests import write_disabled_manifests
from libreprimus.source_delta_audit.git_remote import inspect_remote_tree
from libreprimus.source_delta_audit.image_artifact_backlog import build_image_artifact_observations
from libreprimus.source_delta_audit.source_health import build_source_health_records
from libreprimus.source_delta_audit.tree_classifier import category_counts, selected_path_candidates
from libreprimus.source_delta_audit.variant_comparison import build_variant_comparison_records
from libreprimus.source_delta_audit.validation import write_yaml_records


def run_source_delta_audit(
    *,
    repo_url: str,
    cache_dir: Path,
    out_dir: Path,
    source_delta_out: Path,
    source_health_out: Path,
    image_artifact_out: Path,
    manifest_out_dir: Path,
    allow_network: bool = False,
    allow_warnings: bool = False,
) -> dict[str, Any]:
    """Run Stage 4E metadata-only source delta audit."""

    del allow_warnings
    out_dir.mkdir(parents=True, exist_ok=True)
    tree = inspect_remote_tree(repo_url, cache_dir=cache_dir, allow_network=allow_network)
    counts = category_counts(tree.paths)
    candidates = selected_path_candidates(tree.paths)
    if not candidates and not tree.reachable:
        candidates = [
            {
                "record_type": "source_path_candidate_record",
                "candidate_id": "stage4e-iddqd-remote-deferred",
                "source_id": "stage4e-cicada-solvers-iddqd",
                "path": "remote_tree_unavailable",
                "path_count": 0,
                "sample_paths": [],
                "artifact_type": "remote_tree",
                "source_class": "strong_community_technical",
                "recommended_action": "defer until remote metadata is reachable",
                "duplicate_of": None,
                "raw_file_committed": False,
                "binary_committed": False,
                "font_committed": False,
                "trusted_as_canonical": False,
                "solve_claim": False,
                "notes": "Network access was not allowed or remote tree inspection failed.",
            }
        ]
    variant_records = build_variant_comparison_records(candidates)
    source_delta_records = [
        {
            "record_type": "source_delta_audit_record",
            "audit_id": "stage4e-cicada-solvers-iddqd-tree-delta",
            "source_id": "stage4e-cicada-solvers-iddqd",
            "repo_url": repo_url,
            "remote_head": tree.head,
            "reachable": tree.reachable,
            "path_count": len(tree.paths),
            "category_counts": counts,
            "selected_path_candidates": candidates,
            "variant_comparison_backlog": variant_records,
            "source_class": "strong_community_technical",
            "recommended_action": "source-lock selected paths and queue future comparisons",
            "raw_file_committed": False,
            "binary_committed": False,
            "font_committed": False,
            "trusted_as_canonical": False,
            "solve_claim": False,
            "notes": "Stage 4E records tree metadata only; no repository mirror or raw artefact commit.",
        }
    ]
    source_health = build_source_health_records(
        candidates,
        reachable=tree.reachable,
        remote_head=tree.head,
        repo_url=repo_url,
    )
    image_artifacts = build_image_artifact_observations()
    manifest_paths = write_disabled_manifests(manifest_out_dir)

    write_yaml_records(
        source_delta_out,
        record_set_id="stage4e-cicada-solvers-iddqd-source-delta",
        schema="schemas/history/source-delta-audit-record-v0.schema.json",
        records=source_delta_records,
    )
    write_yaml_records(
        source_health_out,
        record_set_id="stage4e-cicada-solvers-iddqd-source-health",
        schema="schemas/history/source-health-record-v0.schema.json",
        records=source_health,
    )
    write_yaml_records(
        image_artifact_out,
        record_set_id="stage4e-image-compression-artifact-observations",
        schema="schemas/visual/image-compression-artifact-observation-v0.schema.json",
        records=image_artifacts,
    )

    duplicates = [candidate for candidate in candidates if candidate.get("duplicate_of")]
    uniques = [candidate for candidate in candidates if not candidate.get("duplicate_of")]
    warnings = [] if tree.reachable else [{"warning": tree.warning or "remote_unreachable"}]
    _write_jsonl(out_dir / "path_index.jsonl", [{"path": path, "category": _category_for_report(path, counts)} for path in tree.paths])
    _write_jsonl(out_dir / "duplicate_candidates.jsonl", duplicates)
    _write_jsonl(out_dir / "unique_candidates.jsonl", uniques)
    _write_jsonl(out_dir / "warnings.jsonl", warnings)
    summary = {
        "run_id": "stage4e-source-delta-audit",
        "repo_url": repo_url,
        "remote_reachable": tree.reachable,
        "remote_head": tree.head,
        "path_count": len(tree.paths),
        "category_counts": counts,
        "source_delta_records_count": len(source_delta_records),
        "source_health_records_count": len(source_health),
        "duplicate_candidate_count": len(duplicates),
        "unique_candidate_count": len(uniques),
        "image_artifact_records_count": len(image_artifacts),
        "disabled_manifest_count": len([path for path in manifest_paths if path.name != "README.md"]),
        "raw_file_committed": False,
        "binary_committed": False,
        "font_committed": False,
        "generated_outputs_committed": False,
        "solve_claim": False,
        "cuda_used": False,
        "output_paths": {
            "source_delta": source_delta_out.as_posix(),
            "source_health": source_health_out.as_posix(),
            "image_artifact": image_artifact_out.as_posix(),
            "manifest_dir": manifest_out_dir.as_posix(),
            "source_delta_report": (out_dir / "source_delta_report.json").as_posix(),
            "path_index": (out_dir / "path_index.jsonl").as_posix(),
            "duplicate_candidates": (out_dir / "duplicate_candidates.jsonl").as_posix(),
            "unique_candidates": (out_dir / "unique_candidates.jsonl").as_posix(),
            "warnings": (out_dir / "warnings.jsonl").as_posix(),
        },
    }
    (out_dir / "source_delta_report.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return summary


def _category_for_report(path: str, counts: dict[str, int]) -> str:
    del counts
    from libreprimus.source_delta_audit.tree_classifier import classify_path

    return classify_path(path)


def _write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, sort_keys=True) + "\n")
