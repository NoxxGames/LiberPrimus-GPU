"""Stage 4B source-lock triage export orchestration."""

from __future__ import annotations

from pathlib import Path
from typing import Any
import json

from libreprimus.source_lock_triage.disabled_manifests import write_disabled_manifests
from libreprimus.source_lock_triage.loaders import write_yaml_records
from libreprimus.source_lock_triage.negative_controls import build_negative_controls
from libreprimus.source_lock_triage.source_classifier import build_source_records, load_public_links
from libreprimus.source_lock_triage.source_health import build_source_health_records
from libreprimus.source_lock_triage.visual_intake import build_visual_observations, count_by_family


def run_source_lock_triage(
    *,
    stage4a_dir: Path,
    out_dir: Path,
    promoted_sources_out: Path,
    source_health_out: Path,
    visual_observations_out: Path,
    negative_controls_out: Path,
    cookie_source_records_out: Path,
    manifest_out_dir: Path,
    allow_warnings: bool = False,
) -> dict[str, Any]:
    """Run metadata-only Stage 4B triage from Stage 4A generated indexes."""

    del allow_warnings
    out_dir.mkdir(parents=True, exist_ok=True)

    public_links = load_public_links(stage4a_dir)
    promoted_sources, link_summary = build_source_records(public_links)
    source_health = build_source_health_records(promoted_sources)
    visual_observations = build_visual_observations()
    negative_controls = build_negative_controls()
    cookie_records = build_cookie_source_records()
    manifest_paths = write_disabled_manifests(manifest_out_dir)

    write_yaml_records(
        promoted_sources_out,
        record_set_id="stage4b-promoted-source-records",
        schema="schemas/history/stage4b-source-triage-record-v0.schema.json",
        records=promoted_sources,
    )
    write_yaml_records(
        source_health_out,
        record_set_id="stage4b-source-health-records",
        schema="schemas/history/source-health-record-v0.schema.json",
        records=source_health,
    )
    write_yaml_records(
        visual_observations_out,
        record_set_id="stage4b-visual-observation-records",
        schema="schemas/visual/stage4b-visual-observation-record-v0.schema.json",
        records=visual_observations,
    )
    write_yaml_records(
        negative_controls_out,
        record_set_id="stage4b-negative-control-records",
        schema="schemas/research/negative-control-record-v1.schema.json",
        records=negative_controls,
    )
    write_yaml_records(
        cookie_source_records_out,
        record_set_id="stage4b-cookie-candidate-source-records",
        schema="schemas/history/stage4b-source-triage-record-v0.schema.json",
        records=cookie_records,
    )

    rejected_path = out_dir / "rejected_links.jsonl"
    duplicate_path = out_dir / "duplicate_links.jsonl"
    warnings_path = out_dir / "warnings.jsonl"
    report_path = out_dir / "source_triage_report.json"
    _write_jsonl(rejected_path, link_summary.get("rejected_links", []))
    _write_jsonl(duplicate_path, [])
    _write_jsonl(
        warnings_path, [] if public_links else [{"warning": "stage4a_public_link_index_missing"}]
    )

    summary = {
        "run_id": "stage4b-source-lock-triage",
        "stage4a_dir": _display_path(stage4a_dir),
        "stage4a_links_loaded": link_summary["links_loaded"],
        "promoted_source_count": len(promoted_sources),
        "source_health_count": len(source_health),
        "duplicate_links_skipped": link_summary["duplicate_links_skipped"],
        "rejected_unsafe_or_noisy_links": link_summary["rejected_unsafe_or_noisy_links"],
        "ignored_links": link_summary["ignored_links"],
        "visual_observation_count": len(visual_observations),
        "cuneiform_observation_count": count_by_family(visual_observations, "cuneiform_base60"),
        "delimiter_observation_count": count_by_family(
            visual_observations, "mirrored_three_dot_delimiter"
        ),
        "dot_ambiguity_observation_count": count_by_family(
            visual_observations, "dot_binary_ambiguity"
        ),
        "negative_control_count": len(negative_controls),
        "disabled_manifest_count": len(manifest_paths),
        "cookie_source_record_count": len(cookie_records),
        "execution_enabled": False,
        "solve_claim": False,
        "cuda_used": False,
        "raw_outputs_committed": False,
        "generated_outputs_committed": False,
        "output_paths": {
            "source_triage_report": _display_path(report_path),
            "rejected_links": _display_path(rejected_path),
            "duplicate_links": _display_path(duplicate_path),
            "warnings": _display_path(warnings_path),
            "promoted_sources": _display_path(promoted_sources_out),
            "source_health": _display_path(source_health_out),
            "visual_observations": _display_path(visual_observations_out),
            "negative_controls": _display_path(negative_controls_out),
            "cookie_source_records": _display_path(cookie_source_records_out),
            "manifest_dir": _display_path(manifest_out_dir),
        },
    }
    report_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return summary


def build_cookie_source_records() -> list[dict[str, Any]]:
    """Record source-backed cookie candidate families without running hash tests."""

    return [
        {
            "record_type": "stage4b_source_triage_record",
            "source_id": "stage4b-cookie-167-761-exact-artifacts",
            "title": "Stage 4B cookie 167 and 761 exact artefact candidate strings",
            "url": "https://uncovering-cicada.fandom.com/wiki/What_Happened_Part_1_(2014)",
            "normalized_url": "https://uncovering-cicada.fandom.com/wiki/What_Happened_Part_1_(2014)",
            "source_class": "strong_community_technical",
            "classification": "experiment_candidate",
            "evidence_strength": "medium",
            "false_positive_risk": "medium",
            "recommended_action": "queue bounded experiment",
            "stage4a_link_refs": [],
            "retrieval_status": "metadata_recorded_not_fetched_stage4b",
            "trusted_as_canonical": False,
            "solve_claim": False,
            "notes": "Future v2 cookie candidates must be exact public-source strings and deduplicated against prior packs.",
        }
    ]


def _write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, sort_keys=True) + "\n")


def _display_path(path: Path) -> str:
    return path.as_posix()
